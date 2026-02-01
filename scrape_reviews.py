import requests


def scrape_reviews(app_id: int, max_pages=5):
    reviews = []

    for page in range(1, max_pages + 1):
        url = f"https://itunes.apple.com/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        resp = requests.get(url)

        if resp.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        data = resp.json()

        entries = data.get("feed", {}).get("entry", [])

        # First entry is app metadata, skip it
        for entry in entries[1:]:
            rating = int(entry["im:rating"]["label"])
            text = entry["content"]["label"]

            if rating <= 3 and len(text) > 50:
                reviews.append(text)

    return reviews
