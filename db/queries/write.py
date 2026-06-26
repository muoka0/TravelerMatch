import json
from datetime import datetime
from sqlalchemy.orm import Session
from db.schema import Interest, Destination, DestinationInterest, CachedSearch

def insert_interests(session: Session, interest_name: str):
    """Insert a new interest into the interests table during database initialization"""
    
    interest = Interest(interest=interest_name)
    session.add(interest)
    session.commit()    

    return interest

def insert_destinations(session: Session, destination_data: dict):
    """Insert a new destination into the destinations table during database initialization"""
    
    destination = Destination(**destination_data)
    session.add(destination)
    session.commit()

    return destination

def link_destination_interest(session: Session, destination_id: int, interest_id: int):
    """Create a many-to-many relationship between a destination and an interest"""
    
    link = DestinationInterest(
        destination_id = destination_id,
        interest_id = interest_id
    )
    session.add(link)
    session.commit()

def insert_cached_search(
    session: Session,
    query_hash: str,
    start_date: str,
    end_date: str,
    budget_level: str,
    climate: str,
    raw_user_input: str,
    normalized_interests: list[str],
    gemini_output: dict
):
    """Insert a completed Gemini recommendation result into the cache"""
    start_date_obj = datetime.strptime(start_date.strip(), "%Y-%m-%d").date()
    end_date_obj = datetime.strptime(end_date.strip(), "%Y-%m-%d").date()

    cached = CachedSearch(
        query_hash=query_hash,
        start_date=start_date_obj,
        end_date=end_date_obj,
        budget_level=budget_level,
        climate=climate,
        raw_user_input=json.dumps(raw_user_input),
        normalized_interests=json.dumps(normalized_interests),  # store as string
        gemini_output=json.dumps(gemini_output),  # or json.dumps(gemini_output) if JSON field not supported
        created_at=datetime.utcnow()
    )

    session.add(cached)
    session.commit()

    return cached