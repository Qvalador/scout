# *Scout*
#### A Discord bot written with Rapptz's [discord.py](https://github.com/Rapptz/discord.py).
This is the fourth or fifth discord bot i've run through and hopefully the last.  I don't imagine he'll be of much use to anyone else, but he has a cool few tricks that others might benefit from.  See the licence before incorporating any of them for yourself, please.

## Installation

### Requisites
 - [Python 3.5](https://www.python.org/downloads/)
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
 - [gspread](https://github.com/burnash/gspread) (for accessing TGRP moderator records through Google Sheets)
 - [PRAW](https://github.com/praw-dev/praw)
 
I have not included `conf.py` for security reasons.  It's where you'll be placing the majority of your sensitive or machine-specific information.  You may have to do a little bit of reverse engineering to figure out what goes there.  Feel free to contact with me if you have any questions.

### Download
 - Using git: `git clone https://github.com/Qvalador/scout.git`
 - Direct Download: `https://github.com/Qvalador/scout/archive/master.zip`
 
 ***Configure and launch the bot:***

Create and fill `conf.py` in the bot's base directory.  Some things you'll need in there for it to run properly:
 - Your bot's token (`token`)
 - Your bot's cog directory (`cog_dir`)
 - Your bot's base directory (`basedir`)
 
Launch with `python run.py` or `python3 run.py` in your terminal.  `run.py` automatically reboots the bot if it's shut down for whatever reason; if you'd rather have it stay dead, just run `bot.py` instead.

## Known Issues
- The reddit plugin is, as of right now, completely broken.  As far as Scout goes, fixing this is my top priority.  However, working on Scout in general is not really that high on my list of priorities as it stands right now.

## Contact
If you have any questions or concerns, drop them in the bug tracker or catch me on discord at `qvalador#8904`.