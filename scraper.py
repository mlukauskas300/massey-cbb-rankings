import pandas as pd
import requests


def fetch_massey_rankings():
    # Direct backend JSON endpoint used by Massey Ratings for College Basketball
    api_url = "https://masseyratings.com/api/ratings?s=cb&sub=11590"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Extract team rows and column header definitions
    teams = data.get("DI", [])
    cols = data.get("cols", [])

    if not teams:
        print("No ranking data found in the response.")
        return

    # Build header mapping from API definitions
    column_names = ["Team ID", "Team Name"] + [
        c.get("name", f"Col_{i}") for i, c in enumerate(cols)
    ]

    # Convert raw JSON records into a DataFrame
    df = pd.DataFrame(teams)

    # If the column count matches, apply descriptive header titles
    if len(df.columns) == len(column_names):
        df.columns = column_names

    # Save cleanly structured rankings to CSV
    df.to_csv("massey_cbb_rankings.csv", index=False)
    print("Successfully saved massey_cbb_rankings.csv")


if __name__ == "__main__":
    fetch_massey_rankings()
