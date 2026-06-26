from db.connection import SessionLocal, initialize_database
from db.queries.read import (
    get_all_interests, 
    get_cached_search_by_hash, 
    get_destinations_by_constraints, 
    get_unique_climates,
    database_is_empty
)
from db.queries.write import insert_cached_search

from utils.validation import run_validation_pipeline
from utils.cache import generate_cache_key
from utils.scoring import score_destinations, rank_destinations
from utils.seed_db import seed_destinations, seed_interests, seed_destination_interests


from services.gemini_client import (map_interest_to_tags, rank_destinations as gemini_rank_destinations)
from services.weather_client import get_coordinates, get_weather, get_weather_for_locations


def run_pipeline(
    budget_level: str,
    start_date: str,
    end_date: str,
    climate: str,
    interests: list[str]
):

    initialize_database()
    session = SessionLocal()

    try:
        # -----------------------------------------
            # Seed database if empty
        # -----------------------------------------
        if database_is_empty(session):
            seed_destinations(session)
            seed_interests(session)
            seed_destination_interests(session)

            # -----------------------------------------
            # Validate user input
        # -----------------------------------------

        allowed_climates = get_unique_climates(session)

        valid, message = run_validation_pipeline(
            budget=budget_level,
            start_date=start_date,
            end_date=end_date,
            climate=climate,
            interests=interests,
            allowed_climates=allowed_climates
        )
            
        if not valid:
            return {
                "success": False,
                "message": message
            }

        # -----------------------------------------
            # Map user interests using Gemini
        # -----------------------------------------

        mapped_interests = map_interest_to_tags(
            interests
        )

        # -----------------------------------------
            # Generate cache key
        # -----------------------------------------

        query_hash = generate_cache_key(
            budget_level,
            start_date,
            end_date,
            climate,
            mapped_interests
        )

        # -----------------------------------------
            # Check cache
        # -----------------------------------------

        cached_result = get_cached_search_by_hash(
            session,
            query_hash
        )

        if cached_result:
            return cached_result

        # -----------------------------------------
            # Retrieve destinations matching constraints
        # -----------------------------------------

        destinations = get_destinations_by_constraints(
            session=session,
            budget_level=budget_level,
            climate=climate
        )

        # -----------------------------------------
            # Score destinations
        # -----------------------------------------

        scored_destinations = score_destinations(
            destinations,
            mapped_interests
        )

        ranked_destinations = rank_destinations(
            scored_destinations
        )

        # --------------------------------------------------
            # Retrieve weather for ranked destinations
        # --------------------------------------------------

        options_data = []

        for result in ranked_destinations:
            destination = result["destination"]

            weather = get_weather(
                destination.city,
                start_date,
                end_date
            )

            if "error" in weather:
                continue

            weather["country"] = destination.country
            weather["score"] = result["score"]

            options_data.append(weather)

        # --------------------------------------------------
        # Final Gemini recommendation
        # --------------------------------------------------

        user_inputs = {
            "budget": budget_level,
            "climate": climate,
            "interests": ", ".join(mapped_interests)
        }

        recommendations = gemini_rank_destinations(
            user_inputs,
            options_data
            )

        # --------------------------------------------------
            # Store in cache
        # --------------------------------------------------

        insert_cached_search(
            session,
            query_hash=query_hash,
            start_date=start_date,
            end_date=end_date,
            budget_level=budget_level,
            climate=climate,
            raw_user_input=user_inputs,
            normalized_interests=interests,
            gemini_output=recommendations
        )

        return recommendations

    finally:
        session.close()

