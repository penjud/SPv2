#market_data.py
# Example market_data for horse racing
market_data = {
    "horse_form": {
        "recent_performance": ["1st", "2nd", "3rd"],  # List of recent race results
        "wins": 5,
        "losses": 2,
        "consistency": 0.7,  # Consistency score (e.g., based on recent finishes)
    },
    "jockey_performance": {
        "track_record": {
            "total_races": 100,
            "wins": 20,
            "win_percentage": 0.2,
        },
        "recent_wins": 3,  # Jockey's recent wins
    },
    "track_conditions": {
        "weather": "Sunny",
        "track_type": "Turf",  # Turf, dirt, synthetic, etc.
        "distance": "1600m",  # Race distance
    },
    "recent_race_results": [
        {"race_name": "Melbourne Cup", "position": "2nd"},
        {"race_name": "Golden Slipper", "position": "1st"},
        # Add more previous race results
    ],
    "odds": {
        "horse1": 3.5,  # Current odds for each horse
        "horse2": 2.8,
        # Add odds for other horses
    }
}

# Example usage:
horse_name = "horse1"
current_odds = market_data["odds"].get(horse_name, 0)
print(f"Current odds for {horse_name}: {current_odds}")