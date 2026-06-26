from sqlalchemy.orm import Session
from db.schema import Interest, Destination, CachedSearch

def get_all_interests(session: Session):
    """Retrieve all valid interests from the database for Gemini normalization"""
    
    return session.query(Interest).all()

def get_cached_search_by_hash(session: Session, query_hash: str):
    """Retrieve a cached recommendation result using the query hash"""
    
    return session.query(CachedSearch)\
        .filter(CachedSearch.query_hash == query_hash)\
        .first()

def get_destinations_by_constraints(session: Session, budget_level: str, climate: str):
    """Retrieve destinations matching budget, climate, and interest constraints"""
    
    return (
        session.query(Destination)
        .filter(
            Destination.budget_level == budget_level,
            Destination.climate == climate
        )
        .all()
    )

def get_unique_climates(session: Session) -> list[str]:
    climates = (
        session.query(Destination.climate)
        .distinct()
        .all()
    )

    # SQLAlchemy returns tuples like [("temperate",), ("arid",)]
    return [c[0] for c in climates]

def database_is_empty(session: Session) -> bool:
    """
    Returns True if the database has not been seeded yet.
    Uses the destinations table as the indicator.
    """

    return session.query(Destination).first() is None