from services.gemini_client import map_interest_to_tags

def run_interface():
    print("\n--- Travel Match ---\n")

    budget = input("Budget ($, $$, $$$): ").strip()
    climate = input("Preferred climate: ").strip()
    interests = input("What are your interests? ").strip()

    tags = map_interest_to_tags(interests)

    return {
        "budget": budget,
        "climate": climate,
        "interests": interests,
        "tags": tags
    }