def run_interface():
    print(r"""
=============================================================
████████╗██████╗  █████╗ ██╗   ██╗███████╗██╗     ███████╗██████╗
╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔════╝██║     ██╔════╝██╔══██╗
   ██║   ██████╔╝███████║██║   ██║█████╗  ██║     █████╗  ██████╔╝
   ██║   ██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║     ██╔══╝  ██╔══██╗
   ██║   ██║  ██║██║  ██║ ╚████╔╝ ███████╗███████╗███████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝

                    ✈️  TravelerMatch 🌍
          Find your next destination with AI.
=============================================================
""")

    print("Please enter your travel preferences.\n")

    budget = input("Budget ($, $$, $$$): ").strip()
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date (YYYY-MM-DD): ").strip()
    climate = input("Preferred climate: ").strip()
    interests = input("What are your interests? ").strip()

    return {
        "budget": budget,
        "start_date": start_date,
        "end_date": end_date,
        "climate": climate,
        "interests": interests,
    }