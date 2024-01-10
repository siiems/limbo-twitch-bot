# gamba-twitchbot
( Created for onlyvz )
# Prerequisites:
 - Python 3 installed
 - twitchio, psutil, requests  modules

# Setup
- Download code as zip
- Extract into chosen location
- In config.py:
    - Change initial_channel to your desired channel
    - If you want to log the channel message change debug to True
    - Add usernames in lowercase to username_blacklist to blacklist
    - Same goes for userIDs in the userid_blacklist
    - Change prefix as desired
    - Change currency as desired *(emojis are good for this)*
- Add new file called data.json
- Rename token_basic.json to token.json
- In token.json:
    - Add clientid of your bot account to your clientid
    - Change clientsecret
    - Change refresh_token *(access token will appear once script is ran)*
- In a terminal while in the extracted folder, use py bot.py to run the script
- Account userid and username should appear in terminal once succesful
  
# Commands:
  - limbo [bet amount] [multiplier prediction]x | Gamba an amount, cooldown changeable in config.py
  - free | Gives 100 money to user, cooldown changeable in config.py
  -  ping | Displays how long the script has been running and the RAM usage in MB
  -  balance | Displays amount of money the user has
  -  chance [multiplier]x | Display the odds of winning a limbo with the multiplier