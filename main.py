from cli.interface import run_interface
from pipeline.run_pipeline import run_pipeline

def main():
     # Get user input from the CLI
    user_inputs = run_interface()

    # Run the full TravelerMatch pipeline
    recommendations = run_pipeline(
        budget_level=user_inputs["budget"],
        start_date=user_inputs["start_date"],
        end_date=user_inputs["end_date"],
        climate=user_inputs["climate"],
        interests=user_inputs["interests"],
    )

    # Handle validation errors
    if isinstance(recommendations, dict) and not recommendations.get("success", True):
        print(f"\nError: {recommendations['message']}")
        return
    
    # Display recommendations
    print("\n--- Top Matches ---\n")

    for recommendation in recommendations:
        print(f"{recommendation['city']}: {recommendation['reasoning']}")

    print("\nDone.")

if __name__ == "__main__":
    main()