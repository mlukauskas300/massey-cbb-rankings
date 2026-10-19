import pandas as pd
import requests


def fetch_massey_rankings():
    # Massey ratings data URL for CBB
    url = "https://masseyratings.com/cb/ncaa-d1/ratings"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse tables from HTML response
    tables = pd.read_html(response.text)

    if tables:
        df = tables[0]
        # Clean / save dataframe
        df.to_csv("massey_cbb_rankings.csv", index=False)
        print("Successfully updated massey_cbb_rankings.csv")
    else:
        print("No tables found on page.")


if __name__ == "__main__":
    fetch_massey_rankings()
