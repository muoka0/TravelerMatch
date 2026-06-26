
def score_destinations(destinations: list[Destination], interests: list[str]):
    set_of_interest = set(interests)

    scored_destinations = []

    for destination in destinations:
        destination_interests = {
            row.interest.name
            for row in destination.interests
        }

        # determine Jaccard similarity score
        intersection = set_of_interest & destination_interests
        union = set_of_interest | destination_interests
        score = round(len(intersection) / len(union), 2) if union else 0.0

        scored_destinations.append({
            "destination": destination,
            "score": score
        })
    
    return scored_destinations

def rank_destinations(scored_destinations: list[dict], top_k: int = 10):
    return sorted(
        scored_destinations, 
        key=lambda x: x["score"], 
        reverse=True
    )[:top_k] # returns up to the top_k elements