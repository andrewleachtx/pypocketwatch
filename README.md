# pypocketwatch

<img src="resources/seikostarlight.jpg" alt="The watch in question" width="400" style="border-radius: 25px">

Looks through given subreddits on a routine basis and notifies you if anything notable happened.

I don't use the site, but to find what I'm looking for, I would need to use the site every day. Simply put, if a robot does it for me I can spend more time playing Tears of the Kingdom.

In my case, what is notable is the [Seiko Presage "Starlight" SRPC01](https://www.watchgecko.com/blogs/magazine/thoughts-on-the-seiko-presage-cocktail-time-starlight). Not a big watch guy, but after I saw this watch, I am now a big watch guy.

## Constraints
1. Be on one of the subreddits I specify.
2. Be the watch I am looking for (name regex).
3. Only query a reasonable amount per day, the [Reddit API](https://www.reddit.com/dev/api/) has limits.

## How

YouTube, Python [requests](https://pypi.org/project/requests/), and a dream.

I can interpret the data with [regex](https://docs.python.org/3/library/re.html) to see if it is what I am looking for. After finding something I want, I can use check for ${...} and find their price as well as other info about the post.

I am using [sqlite3](https://docs.python.org/3/library/sqlite3.html) as a lightweight container for my results. I can also store the last date queried, so I don't overquery.