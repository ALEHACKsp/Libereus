![discord](https://discordapp.com/api/guilds/445157253385814016/widget.png?style=shield)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
# Libereus
Libereus is a Discord bot written in Python 3 as a submission to participate in the Moderation category of [Discord Hack Week 2019](https://blog.discordapp.com/discord-community-hack-week-build-and-create-alongside-us-6b2a7b7bba33).

It has the ability to:
> ✅ Prune inactive members via their last message's date  
> ✅ Disable or re-enable messaging permissions on a given channel for normal members  
> ✅ Zalgo spam messages removal  
> ✅ Remove a prefix from members' nicknames (i.e. usage of `!` to hoist to the top of the member list)  
> ✅ 💣 GENERATE A COOL SPOILER-MINESWEEPER GAME 💣  
> ...and much more!

## Developers
`Tansc#8171` `Proladon#7525` `NRockhouse#4157`

## Requirements
> 🐍 Python 3.7

## Installation
### Registering an access token for your bot
1. Navigate to [Discord Developer Portal (Applications)](https://discordapp.com/developers/applications/).
1. Click on "New Application".  
![](https://i.imgur.com/5SSK14E.jpg)
1. Fill in a name for your bot (or just "Libereus"), and click on Create.
1. Click on "Bot" at the left navigation panel, and then "Add Bot".
1. Next, click on "Click to Reveal Token" in the "Build-A-Bot" section and write down the token somewhere, it is required for the installation later. (DO NOT SHARE YOUR TOKEN WITH ANY OTHER PEOPLE, NOT EVEN ANIMALS!)
1. Now click on "OAuth2" on the left navigation panel, scroll down to "Scopes" and then tick on "bot".
1. Scroll further down to find "Bot Permissions" and check on "Administrator".
1. You can now proceed to copy the generated link in the "Scopes" section and open the link in your web browser.
![](https://i.imgur.com/V5kwpNN.jpg)
1. Add the bot into your server through the page.

### Windows
Allan please add details

###  Mac
> Unfortunately, this bot requires Python 3 but Mac OS X / macOS ships with Python 2.7 out of the box, thus you need to install Python 3 seperately to run this bot.
1. Open the "Terminal" application.
1. Install [Homebrew](https://brew.sh/) via the following command.  
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
1. Install Python 3 by entering the command.  
`brew install python3`
1. 

### 🐧 Linux


## Commands
### 🔥 Prunemembers (Lack of messages / inactive)
![img](https://i.imgur.com/rv4vWvW.gif)

> _*If your server has hundreds or thousands of members, it may take a very long time to search.*_
```
/prunemembers <days> <option: include_no_message= true(1)/false(0). default=false(0)>
```

### 📅 Calculate Date
![img](https://i.imgur.com/4gRlUrZ.gif)
