import requests
from datetime import datetime, timedelta
import pytz

# Make work with multiple later.
subreddit = "Watchexchange"
search_term = "Seiko"
limit = 1000

# We should query only yesterday, today
end_date = datetime.now()
start_date = end_date - timedelta(days=1)
start_timestamp = int(start_date.timestamp())
end_timestamp   = int(end_date.timestamp())

# You can play with the parameters at the end by templating
# Get 20 new posts off of given subreddit
url = f"https://www.reddit.com/r/{subreddit}/search.json?q={search_term}&restrict_sr=1&sort=new&limit={limit}&after={start_timestamp}&before={end_timestamp}"

# params = {
#     "q": search_term,
#     "restrict_sr": 1,
#     "sort": "new",
#     "limit": limit,
#     "after": start_timestamp,
#     "before": end_timestamp
# }

# url = f"https://www.reddit.com/r/{subreddit}/search.json"

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

        print(f"post_id = {post_id}")
        print(f"title = {title}")
        print(f"score = {score}")
        print(f"author = {author}")
        cdt_timezone = pytz.timezone("America/Chicago")
        date = datetime.utcfromtimestamp(date)
        date = cdt_timezone.localize(date)
        print(f"date = {date}")
        print(f"url = {url}")
        print("-" * 20)
else:
    print(f"Request failed -- Error {response.status_code}")

def main():
    pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"Exiting")