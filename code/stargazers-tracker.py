import requests
import json
import os

data_file = "stargazers5.json"


def get_repositories(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break
            repos.extend([repo['name'] for repo in batch])
            page += 1
        else:
            break
    return repos


def get_stargazers(username, repo):
    stargazers = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{username}/{repo}/stargazers?per_page=100&page={page}"
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
        if response.status_code == 200:
            batch = response.json()
            if not batch:
                break
            stargazers.extend([user['login'] for user in batch])
            page += 1
        else:
            break
    return stargazers


def load_previous_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)


def track_new_stargazers(username):
    previous_data = load_previous_data()
    if username not in previous_data:
        previous_data[username] = {}

    current_data = {}
    new_stargazers = {}

    repos = get_repositories(username)
    for repo in repos:
        current_stars = set(get_stargazers(username, repo))
        old_stars = set(previous_data[username].get(repo, []))

        if repo not in previous_data[username]:
            new_users = current_stars  # all stars are considered new if repo wasn't tracked before
        else:
            new_users = current_stars - old_stars

        if new_users:
            new_stargazers[repo] = list(new_users)
        current_data[repo] = list(current_stars)

    previous_data[username] = current_data
    save_data(previous_data)

    if new_stargazers:
        print(f"New stargazers detected for {username}:")
        for repo, users in new_stargazers.items():
            print(f"Repo: {repo}, New Stargazers: {', '.join(users)}")
    else:
        print(f"No new stargazers found for {username}.")


if __name__ == "__main__":
    target_username = input("Enter the GitHub username to track: ")
    track_new_stargazers(target_username)
