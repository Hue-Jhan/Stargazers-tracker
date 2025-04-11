import requests
import json
import os

github_username = "Hue-Jhan"
storage_file = "stargazers.json"


def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo['name'] for repo in response.json()]
    return []


def get_stargazers(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/stargazers"
    response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    if response.status_code == 200:
        return [user['login'] for user in response.json()]
    return []


def load_previous_data():
    if os.path.exists(storage_file):
        with open(storage_file, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(storage_file, "w") as f:
        json.dump(data, f, indent=4)


def track_new_stargazers():
    previous_data = load_previous_data()
    current_data = {}
    new_stargazers = {}

    repos = get_repositories(github_username)
    for repo in repos:
        current_stars = set(get_stargazers(github_username, repo))
        old_stars = set(previous_data.get(repo, []))
        new_users = current_stars - old_stars
        if new_users:
            new_stargazers[repo] = list(new_users)
        current_data[repo] = list(current_stars)

    save_data(current_data)

    if new_stargazers:
        print("New stargazers detected:")
        for repo, users in new_stargazers.items():
            print(f"Repo: {repo}, New Stargazers: {', '.join(users)}")
    else:
        print("No new stargazers found.")


if __name__ == "__main__":
    track_new_stargazers()
