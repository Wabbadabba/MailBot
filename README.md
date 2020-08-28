# MailBot

This is a Discord Bot made in Python 3.8. It is intended for a homebrew Dungeons & Dragons Server, but can be edited quickly to adapt to any use-case. 

### Prerequisites

This bot uses Discord.py, dotenv, and its extention discord-flags

```
pip install -U discord.py
```
```
pip install discord-flags
```
```
pip install -U python-dotenv
```

Alternatively, you can use the [mailbot-requirements.txt](https://github.com/Wabbadabba/MailBot/blob/master/mailbot-requirements.txt) to install all dependencies
```
pip install -r mailbot-requirements.txt
```

## Commands
Command | Description
------- | -----------
`m.mList` | Shows a list of all valid recipients
`m.addList` | Adds a new entry into the list of valid recipients
`m.send` | Picks a random number between 1 and 20, and sends a message if the number is above 3.
`m.help` | Displays help information.

## Built With

* [Discord.py](https://discordpy.readthedocs.io/en/latest/) - The Discord API framework used
* [Discord-flags](https://pypi.org/project/discord-flags/) - Allows flags to be passing into commands

## Authors

* **Shawn Wabschall** - *Initial work* - [Wabbadabba](https://github.com/Wabbadabba)
