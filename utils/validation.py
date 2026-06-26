from datetime import datetime

def validate_budget(budget: str) -> bool:
    allowed = {"$", "$$", "$$$"}

    return budget.strip() in allowed

def validate_dates(start_date: str, end_date: str) -> tuple[bool, str]:
    try:
        start = _parse_date(start_date).date()
        end = _parse_date(end_date).date()
        today = datetime.today().date()
    
        # check if the dates are in chronological order
        if start > end:
            return False, "The travel start date must be before the travel end date."
        
        # check if the dates are in the past
        if start < today or end < today:
            return False, "The travel dates cannot be in the past."
        
        return True, ""

    except ValueError:
        return False, "Dates must be in YYYY-MM-DD format"

def _parse_date(date: str) -> datetime:
    DATE_FORMAT = "%Y-%m-%d"

    return datetime.strptime(date.strip(), DATE_FORMAT)

def validate_climate(climate: str, allowed_climates: list[str]):
    return climate.strip().lower() in {
        climate.lower() for climate in allowed_climates
    }

def validate_interests(interests: list[str]) -> bool:
    if not interests:
        return False

    cleaned = [interest.strip().lower() for interest in interests if interest.strip()]

    return len(cleaned) > 0 # ensure a non-empty string for the gemini input

def run_validation_pipeline(
    budget: str,
    start_date: str,
    end_date: str,
    climate: str,
    interests: list[str],
    allowed_climates: list[str]
) -> tuple[bool, str]:
    
    if not validate_budget(budget):
        return False, "Invalid budget (must be $, $$, or $$$)"

    valid_dates, date_msg = validate_dates(start_date, end_date)
    if not valid_dates:
        return False, date_msg

    if not validate_climate(climate, allowed_climates):
        return False, "Invalid climate selection"

    if not validate_interests(interests):
        return False, "Interests cannot be empty"

    return True, ""
