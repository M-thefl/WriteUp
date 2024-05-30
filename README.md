# 📝 Write-Up Bot

Write-Up Bot is a Python script that automatically checks various RSS feeds related to cybersecurity, bug bonuses and hacks. It collects the latest entries and sends them to a Discord and Telegram channel

## ✨ Features

- 📡 **Data Collection from RSS Feeds:** The script fetches links and descriptions of new write-ups from specified RSS feeds.
- 💾 **Database Storage:** The fetched information is stored in a SQLite database.
- 🚀 **Automated Discord Notifications:** New write-ups are automatically sent to a Discord channel using embeds.
- ⏳ **Delay Mechanism:** Includes a delay to prevent spamming the Discord and Telegram channel with multiple notifications in quick succession.

## 📋 Requirements

- Python 3.x
- `requests` library
- `lxml` library
- `sqlite3` library
- `logging` library

## ⚙️ Configuration
Create a config.json file in the data directory with the following structure:

```json
{
    "Discord": {
      "WebHook": "YOUR_DISCORD_WEBHOOK_URL"
    },
    "Telegram": {
        "BotToken": "YOUR_TELEGRAM_BOT_TOKEN",
        "ChatID": "YOUR_TELEGRAM_CHAT_ID"
    },
    "Database": {
      "FilePath": "SQL/database.db"
    "TagURLs": [
        "https://medium.com/feed/tag/bug-bounty-writeup",
        "https://medium.com/feed/tag/cybersecurity",
        "https://medium.com/feed/tag/application-security",
        ...
    ]
}
```
## 🛠️ Usage
1. Clone the repository:
```bash
git clone https://github.com/M-thefl/WriteUp.git
cd WriteUp
pip install -r requirements.txt
```
 2. Configure the bot:<br>
 `Update config.json file with your Discord website address, Telegram BotToken, ChatID and RSS feed URLs.`

3. Run the script:
`python main.py`
   
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🖋 Contact
If you have any questions or suggestions, feel free to contact me at Mahbodfl1@gmail.com

``good luck (; 🌙``<br />
``for life``<br />
``fl``
🚀


