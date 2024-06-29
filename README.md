# pypocketwatch
## May 2024
A daily crontab-executed Python script running on Raspberry Pi 4 (Watson) to scrape, filter, and report noise on Reddit relating to the sale of the Seiko SARY085/SRPC01J1, my favorite watch.

<img src="resources/seikostarlight.png" alt="The watch in question" width="400" style="border-radius: 25px">

Have you ever seen something, and for once it just made sense? I am by far not a watch guy, and I don't really have a big eye for pricy things. But I like to think about the idea that I can one day get this. It's a goal, not a dream.

The watch I am referring to is the Seiko Presage "Starlight" SRPC01J1.

There is a version with many more complications, which is the Seiko SSA361J1. I like this one too.


## Table of Contents
- [pypocketwatch](#pypocketwatch)
  - [May 2024](#may-2024)
  - [Table of Contents](#table-of-contents)
  - [The Problem](#the-problem)
  - [How](#how)
  - [Constraints](#constraints)
  - [Automation](#automation)
  - [Reaching Out (Notifications)](#reaching-out-notifications)
  - [Price Points](#price-points)
  - [Cool Pictures](#cool-pictures)
  - [Future](#future)
  - [Technologies](#technologies)


## The Problem
Looking for niche items yields unpredictable sales patterns across any trade. If you check each day for 150 days straight, you may skip day 151 and miss the sale. This means you must check daily. 

I don't want to do daily checks through multiple online pages for sales information and whatever else is associated with this specific watch. It is unfeasible; too many pages, I make mistakes, get bored, etc.

Simply put, if a ~~robot~~ [Watson](#automation) does it for me, I know I can trust the objectivity and conciseness of the information. Now I have more time for what I love to do.


## How
YouTube tutorials, my favorite Python [requests](https://pypi.org/project/requests/) library, and a dream.

I can interpret the data with [regex](https://docs.python.org/3/library/re.html) to see if it is what I am looking for. After finding something I want, I can use check for ${...} and find their price as well as other info about the post.

I am using [sqlite3](https://docs.python.org/3/library/sqlite3.html) as a lightweight container for my results. I can also store the last date queried, so I don't overquery.


## Constraints
1. Be on one of the subreddits I specify.
2. Be the watch I am looking for (name regex).
3. Only query a reasonable amount per day, the [Reddit API](https://www.reddit.com/dev/api/) has "limits".


## Automation
I could probably get this script running with [GitHub Actions](https://docs.github.com/en/actions) or something, but I've been letting **this guy** sit around collecting dust.

(this guy, now named **Watson**.)

<img src="resources/rpi4.png" alt="Raspberry Pi 4" width="350" style="border-radius: 25px">

Glad I took the time to set [Watson](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) up (he has been waiting 5 years) as now I have a server I can ssh into and work from on my local machine for free (omitting power).

My mind races at what else I can do now, but I'll keep it to this project.

I knew there was some process system task scheduler, and Google yielded [crontab](https://www.geeksforgeeks.org/crontab-in-linux-with-examples/), which was simple enough for setting up a basic script to run. This was the only line I added in my `crontab -e`:

```sh
0 0 * * * /usr/bin/python3 /longpathfromroot/Desktop/fun/pypocketwatch/src/main.py
```

For now, it will run at midnight every day, updating (only as necessarily) a local database as needed. There is no concern for local RPI4 storage, because of some nice "update on unique" logic I have included.


## Reaching Out (Notifications)
I don't want to look, Watson should look and tell me. There are plethora of ways to send notifications, I decided to go with [Pushover](https://pushover.net/) for now.

If you look in src/main.py you will notice the use of a .env file which stores information specific to me that I felt wouldn't be the smartest to put in a public repo.

You can probably deduce what everything does. Basically, I make a POST request to the Pushover API with my info, and it will handle everything for me. Most of my work was getting a good message set up.


## Price Points
TBD?


## Cool Pictures
(Watson + beautiful cable management)

<img src="resources/watson.png" alt="watsonnn" width="400" style="border-radius: 25px">

(Database - It works?!?!)

<img src="resources/dbexample.png" alt="sqlite3 db example" style="border-radius: 25px">

I thought there'd be more cool pictures but I guess I can do a better job of documenting next time. This was cool though, ask me about it.


## Future
- [x] ~~Make it reach out to me if something happens, so I don't even have to check.~~ [done](#reaching-out-notifications)
- [ ] Add more columns or additional parsing to store price point if it is ACTUALLY the watch.
- [ ] Wait... even with this, I have no money...
- [ ] Get more money (hire me?)


## Technologies
- Python
  - SQLite3, requests, regex, logging
- Raspberry Pi 4
  - the manual, lol; linux + os & knowledge; ssh + keygen, crontab
- The Internet
  - [Reddit API](https://www.reddit.com/dev/api/)
  - [YouTube](https://www.youtube.com/)
  - [Tutorial / wireframe for parsing reddit](https://www.youtube.com/watch?v=Se3GEUY3AGI)
  - [This guy's rpi cheatsheet](https://github.com/LukaszLapaj/raspberry-pi-cheat-sheet)
  - [.env refresher for Python](https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/)
  - [Push notification API](https://pushover.net/api#priority)
