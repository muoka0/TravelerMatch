import hashlib

def generate_cache_key(
    budget_level: str,
    start_date: str,
    end_date: str,
    climate: str,
    interests: list[str]
):
    # normalize user inputs
    norm_budget, norm_start_date, norm_end_date, norm_climate, norm_interests = _normalize_constraints(
        budget_level, start_date, end_date, climate, interests)

    # create canonical string
    canonical_string = _create_canonical_string(
        norm_budget, norm_start_date, norm_end_date, norm_climate, norm_interests
    )

    # create hash of canonical string
    query_hash = _create_query_hash(canonical_string)

    return query_hash


def _normalize_constraints(budget_level: str, start_date: str, end_date: str, climate: str, interests: list[str]):
    # clean up user input, remove whitspace and make all chars lowercase
    budget_level = budget_level.strip()
    start_date = start_date.strip()
    end_date = end_date.strip()
    climate = climate.strip().lower()

    # sort interests to ensure consistent ordering, removes duplicates
    interests = sorted({
        interest.strip().lower()
        for interest in interests
    })

    return budget_level, start_date, end_date, climate, interests


def _create_canonical_string(budget_level: str, start_date: str, end_date: str, climate: str, interests: list[str]):
    '''
    The string must hold this format:
        - budget=$$
        - start=2026-08-01
        - nd=2026-08-10
        - climate=temperate
        - interests=food,hiking,nightlife
    each section separated by |
    '''
    canonical_string = f"budget_level={budget_level}|start_date={start_date}|end_date={end_date}|climate={climate}|interests={','.join(interests)}"

    return canonical_string


def _create_query_hash(canonical_string: str):
    return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()
