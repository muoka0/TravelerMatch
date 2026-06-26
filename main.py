from cli.interface import run_interface
from services.gemini_client import rank_destinations

def main():
    options_data = [
        {
            "city": "Bali",
            "avg_high": 89.0,
            "avg_low": 69.3,
            "avg_daily_rain_mm": 1.8
        },
        {
            "city": "Bangkok",
            "avg_high": 95.0,
            "avg_low": 75.0,
            "avg_daily_rain_mm": 0.5
        }
    ]

    user_inputs = run_interface()

    ranked = rank_destinations(user_inputs, options_data)

    print("\n--- Top Matches ---\n")
    for r in ranked:
        print(f"{r['city']}: {r['reasoning']}")

    print("\nDone. Summary:")
    print({**user_inputs, "ranked": ranked})

if __name__ == "__main__":
    main()