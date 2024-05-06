import requests
from datetime import datetime
import pytz
import sqlite3

def gen_table(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            date REAL,
            subreddit TEXT,
            url TEXT,
            score INTEGER
        )
        """
    )

    conn.commit()

# We should just keep querying because we can't get all the posts at once.
def parse(subreddit, after="", limit=1000, search_term="", conn=None):
    url = f"https://www.reddit.com/r/{subreddit}/search.json"

    params = {
        "q": search_term,
        "restrict_sr": 1,
        "sort": "new",
        "limit": limit,
        "t": "month",
        "after": after
    }

    print(f"Searching for {search_term} in r/{subreddit} with after={after}, limit={limit}")

    headers = {
        "User-Agent": "pypocketwatcha"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        c = conn.cursor()
        data = response.json()["data"]

        for post in data["children"]:
            post_data = post["data"]

            post_id = post_data["id"]
            title = post_data["title"]
            score = post_data["score"]
            author = post_data["author"]
            date = post_data["created_utc"]
            url_ow = post_data.get("url_overridden_by_dest")

            date = datetime.utcfromtimestamp(date)
            date = pytz.utc.localize(date).astimezone(pytz.timezone("America/Chicago"))
            formatted_date = date.strftime("%Y-%m-%d %I:%M %p")

            c.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)",
                (post_id, title, author, formatted_date, subreddit, url_ow, score))

        conn.commit()

        # return back "after" so we can update params["after"] in the next request
        return response.json()["data"]["after"]
    else:
        print(f"Request failed -- Error {response.status_code}")
        return None

def main():
    subreddits = ["Watchexchange", "watch_swap", "Watches", "Seiko"]

    conn = sqlite3.connect("../resources/pypocketwatch.db")
    gen_table(conn)

    max_pages = 10

    after = ""
    for subreddit in subreddits:
        for i in range(1, max_pages + 1):
            try:
                print(f"Parsing r/{subreddit} in the last <week>, page {i}")
                after = parse(subreddit, after=after, search_term="Seiko", conn=conn)

                if not after:
                    print("No after")
                    break
            except KeyboardInterrupt:
                print(f"Exiting on keyboard interrupt")
                break

    conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"Exiting")