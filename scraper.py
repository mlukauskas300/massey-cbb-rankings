import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def fetch_massey_rankings():
    url = "https://masseyratings.com/ranks?s=cb"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_selector("table", timeout=30000)

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tables = pd.read_html(str(soup))

    if not tables:
        raise ValueError("No tables were found on the rendered page.")

    df = max(tables, key=lambda t: len(t))
    df.columns = [str(col).strip() for col in df.columns]
    df.dropna(how="all", inplace=True)

    df.to_csv("massey_cbb_rankings.csv", index=False)
    print("Successfully saved massey_cbb_rankings.csv")


if __name__ == "__main__":
    fetch_massey_rankings()
