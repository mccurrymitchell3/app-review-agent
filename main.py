import os
from dotenv import load_dotenv

from scrape_reviews import scrape_reviews
from analyze_reviews import analyze_reviews
from create_github_issues import create_github_issues

load_dotenv()

APP_ID = int(os.getenv("APP_ID"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def main():
    print("Scraping reviews...")
    reviews = scrape_reviews(APP_ID)

    print(f"Collected {len(reviews)} reviews")
    if not reviews:
        return

    print("Analyzing reviews with Ollama...")
    issues = analyze_reviews(reviews)

    if not issues:
        print("No issues found.")
        return

    print(f"Creating {len(issues)} GitHub issue(s)...")
    create_github_issues(GITHUB_REPO, GITHUB_TOKEN, issues)

    print("Done.")


if __name__ == "__main__":
    main()
