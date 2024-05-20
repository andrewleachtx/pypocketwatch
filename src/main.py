#!/usr/bin/env python3
import logging
import os
import re
import sqlite3
from datetime import datetime
from http import HTTPStatus

import pytz
import requests
from dotenv import load_dotenv

load_dotenv()

CUR_DIR        = os.path.dirname(os.path.abspath(__file__))
LOG_DIR        = os.path.join(CUR_DIR, "../logs/")
RESOURCES_DIR  = os.path.join(CUR_DIR, "../resources/")

STRFTIME_FORMAT = "%B %d, %Y %I:%M %p"

# Pushover API stuff
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_ID   = os.getenv("PUSHOVER_USER_ID")
PUSHOVER_DEVICE_ID = os.getenv("PUSHOVER_DEVICE_ID")

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

# Posts HTTP request to pushover.net API
def sendNotification(message):
    params = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_ID,
        "device": PUSHOVER_DEVICE_ID,
        "title": f"pypocketwatch -- {len(new_entries)} new entries at {datetime.now().strftime(STRFTIME_FORMAT)}",
        "message": message
    }

    response = requests.post(PUSHOVER_URL, data=params)

    if response.ok:
        logging.log(logging.INFO, f"Push noti successfully sent")
    else:
        logging.log(logging.WARNING, f"Push noti failed")

    return response.ok == True

# for this iteration of the script
new_entries = []

def genTable(conn):
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

def filterTitle(title: str) -> bool:
    """
        we are looking for unique identifiers like

        starlight, scrp01, sary085
    """

    pattern = r"(?:starlight|scrp01|sary085|cocktail|cocktail time)"

    match = re.search(pattern, title, re.IGNORECASE)

    return bool(match)

# We should just keep querying because we can't get all the posts at once.
def parse(subreddit, after="", limit=1000, search_term="", conn=None):
    url = f"https://www.reddit.com/r/{subreddit}/search.json"

    params = {
        "q": search_term,
        "restrict_sr": 1,
        "sort": "new",
        "after": after
    }

    # <platform>:<app ID>:<version string> (by u/<username>)
    headers = {
        "User-Agent": f"python3:pypocketwatch (by /u/{REDDIT_USERNAME})"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        c = conn.cursor()
        data = response.json()["data"]

        for post in data["children"]:
            post_data = post["data"]

            post_id = post_data["id"]
            # before we do anything else check if the post already exists
            c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
            if c.fetchone():
                continue

            title = post_data["title"]

            # fine tuned filtering
            if not filterTitle(title):
                continue

            score = post_data["score"]
            author = post_data["author"]
            date = post_data["created_utc"]
            url_ow = post_data.get("url_overridden_by_dest")

            date = datetime.utcfromtimestamp(date)
            date = pytz.utc.localize(date).astimezone(pytz.timezone("America/Chicago"))
            formatted_date = date.strftime("%Y-%m-%d %I:%M %p")

            new_entries.append([title, author, formatted_date, subreddit, url_ow])

            c.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)",
                (post_id, title, author, formatted_date, subreddit, url_ow, score))

        conn.commit()

        # return back "after" so we can update params["after"] in the next request
        return response.json()["data"]["after"]
    elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        logging.warning(f"Request failed due to {response.status_code}, too many requests being sent")
    else:
        print(f"Request failed - Error {response.status_code}")
        return None

def main():
    subreddits = ["Watchexchange", "watch_swap", "Watches", "Seiko"]
    searches   = ["seiko", "starlight", "seiko starlight", "scrp01"]

    conn = sqlite3.connect(f"{RESOURCES_DIR}/pypocketwatch.db")
    genTable(conn)

    max_pages = 15

    # touch all bases
    for search_term in searches:
        for subreddit in subreddits:
            print("-" * 50)
            print(f"Parsing r/{subreddit} in the last <week> for max {max_pages} pages")

            after = ""
            for i in range(1, max_pages + 1):
                try:
                    print(f"\tPage {i} of r/{subreddit} with after={after}")
                    after = parse(subreddit, after=after, search_term=search_term, conn=conn)

                    if not after:
                        print(f"Ended parsing @ page {i}: No after token found")
                        break

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

    conn.close()

if __name__ == "__main__":
    try:
        logging.basicConfig(filename=f"{LOG_DIR}/main.log", level=logging.INFO)

        start = datetime.now()
        logging.info(f"Script starting @ {start.strftime(STRFTIME_FORMAT)}")

        main()


        end = datetime.now()
        logging.info(f"\t{new_entries} new entries found, took {(end - start)}")

        if new_entries:
            full_message = [f"pypocketwatch -- task complete @ {end.strftime(STRFTIME_FORMAT)} with {len(new_entries)} new entries found:"]

            for entry in new_entries[:15]:
                full_message.append(f"\t{entry[0]} by {entry[1]} on {entry[2]} in r/{entry[3]}")
                full_message.append(f"\t{entry[4]}")

            if len(new_entries) > 15:
                full_message.append(f"\t... and omitting {len(new_entries) - 10} more entries, view database locally")

            sendNotification("\n".join(full_message))

        logging.info(f"Script ended @ {end.strftime(STRFTIME_FORMAT)}")

    except KeyboardInterrupt:
        print(f"Exiting on keyboard interrupt")