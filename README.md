# gamba-twitchbot
*( Created for onlyvz )*
# Description
Small(ish) twitch bot for a chat-based game
Has basic QOL features and changeable values

# Prerequisites:
 - **Python 3** installed
 - **twitchio**, **psutil**, **requests**  modules
 - Twitch **ClientID**, **ClientSecret** and **RefreshToken** *( see the [Twitch Developer Authentication Page](https://dev.twitch.tv/docs/authentication/) )*

# Setup
- Download code as zip
- Extract into chosen location
- In **config.py**:
    - Change **initial_channel** to your desired channel
    - If you want to log the channel message change **debug** to *True*
    - Add usernames in lowercase to **username_blacklist** to **blacklist**
    - Same goes for **userID**s in the **userid_blacklist**
    - Change **prefix** as desired
    - Change **currency** as desired __(emojis are good for this)__
- Add new file called **data.json**
- Rename **token_basic.json** to **token.json**
- In **token.json**:
    - Add *clientid* of your bot account to your **clientid**
    - Change **clientsecret**
    - Change **refresh_token** *(access token will refresh itself once script is ran)*
- In a terminal while in the extracted folder, use **py bot.py** to run the script
- Account **userid** and **username** should appear in terminal once successful


# Commands:
  - **limbo** *[bet amount]* *[multiplier prediction]*x | Gamba an amount, cooldown changeable in config.py
  - **free** | Gives 100 money to user, cooldown changeable in config.py
  - **ping** | Displays how long the script has been running and the RAM usage in MB
  - **balance** | Displays amount of money the user has
  - **chance** *[multiplier]*x | Display the odds of winning a limbo with the multiplier
  - **leaderboard** | Shows users rank compared to total users, ranked by total money
  - **give** *[userid]* *[amount]* | Gives user with the given userid the specified amount of money

# Config
Most things you could want to change about the bot can be changed in config.py, such as:
 - Command prefix
 - Initial channel that the bot connects to, once the script is ran
 - Debug Mode (turns logging of messages on or off)
 - Username or UserID blacklist, (using userID blacklist is recommended as usernames can change)
 - Cooldown for limbo command
 - Cooldown for free command
 - Currency that is displayed in bot messages (can be emojis, standard currency symbols or anything you want really)
 - Chance of a pre 1x roll crash for limbo command, increase odds to deter spamming low rolls
 (don't touch the last thing in config)

