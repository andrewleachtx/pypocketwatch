import requests
from pprint import pprint

# Make work with multiple later.
subreddit = "Watchexchange"

# You can play with the parameters at the end
url = f"https://www.reddit.com/r/{subreddit}/top.json?t=all"

headers = {
    "User-Agent":  "pypocketwatcha"
}

response = requests.get(url, headers=headers)

if response.ok:
    data = response.json()["data"]

    for post in data["children"]:
        post_data = post["data"]

        post_id   = post_data["id"]
        title     = post_data["title"]
        score     = post_data["score"]
        author    = post_data["author"]
        date      = post_data["created_utc"]
        url       = post_data.get("url_overridden_by_dest")

        # print(f"Post ID: {post_id}")
        # print(f"Title: {title}")
        # print(f"Author: {author}")
        # print(f"Date: {date}")
        # print(f"URL: {url}")
        # print("-" * 20)
else:
    print(f"Request failed -- Error {response.status_code}")