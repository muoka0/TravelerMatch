from cli.interface import run_interface
from services.gemini_client import map_interest_to_tags, rank_destinations

def main():
    user_inputs = run_interface()

    tags = map_interest_to_tags(user_inputs["interests"])
    user_inputs["interests"] = ", ".join(tags)

    result = rank_destinations(user_inputs, user_inputs["options_data"])

    print(result)

if __name__ == "__main__":
    main()