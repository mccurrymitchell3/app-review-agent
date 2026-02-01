import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
REQUIRED_KEYS = {"issue_title", "description", "mentions", "examples"}

def validate_issue(issue):
    return REQUIRED_KEYS.issubset(issue.keys())


def normalize_issues(data):
    # If model returned {"issues": [...]}
    if isinstance(data, dict) and "issues" in data:
        return data["issues"]

    # If model returned already a list
    if isinstance(data, list):
        return data

    # If model returned only one issue object with no list
    if isinstance(data, dict) and "issue_title" in data:
        return [data]

    # Otherwise unexpected format
    print(data)
    raise ValueError("Unexpected JSON format from LLM")


def analyze_reviews(reviews: list[str]) -> list[dict]:
    prompt = f"""
        You are a product manager.

        Analyze the following user reviews and extract the top recurring issues or complaints.

        Return ONLY valid JSON in this format:

        [
        {{
            "issue_title": "short title",
            "description": "clear description",
            "mentions": number,
            "examples": ["quote1", "quote2"]
        }}
        ]

        Reviews:
        {json.dumps(reviews[:50], indent=2)}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
    )

    result = response.json()["response"]

    try:
        parsed = json.loads(result)
        issues = normalize_issues(parsed)
        issues = [i for i in issues if validate_issue(i)]
    except json.JSONDecodeError:
        print("LLM output was not valid JSON:")
        print(result)
        return []

    return issues
