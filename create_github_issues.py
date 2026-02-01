from github import Github


def format_examples(examples):
    cleaned = []
    for e in examples:
        # remove internal newlines and extra spaces
        line = " ".join(e.split())
        line = line[:300] + "..." if len(line) > 300 else line
        line = line.strip()
        cleaned.append(f"- {line}")
    return "\n".join(cleaned)


def create_github_issues(repo_name: str, token: str, issues: list[dict]):
    g = Github(token)
    repo = g.get_repo(repo_name)

    for issue in issues:
        print(issue)
        title = issue["issue_title"]
        body = f"""
## Description
{issue['description']}

## Mentions
{issue['mentions']}

## Example Reviews
{format_examples(issue['examples'])}
"""

        repo.create_issue(title=title, body=body)
        print(f"Created issue: {title}")
