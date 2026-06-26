def run_interface():
    print("\n--- Travel Match ---\n")

    budget = input("Budget ($, $$, $$$): ").strip()
    climate = input("Preferred climate: ").strip()
    interests = input("What are your interests? ").strip()
    
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

    return {
        "budget": budget,
        "climate": climate,
        "interests": interests,
        "options_data": options_data
    }