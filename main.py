import json
import time
from lxml import etree
import requests
import sqlite3
import logging
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Print  banner
print(f'''{Fore.MAGENTA}
 /$$      /$$           /$$   /$$               /$$   /$$                  /$$$$$$                      /$$             /$$    
| $$  /$ | $$          |__/  | $$              | $$  | $$                 /$$__  $$                    |__/            | $$    
| $$ /$$$| $$  /$$$$$$  /$$ /$$$$$$    /$$$$$$ | $$  | $$  /$$$$$$       | $$  \__/  /$$$$$$$  /$$$$$$  /$$  /$$$$$$  /$$$$$$  
| $$/$$ $$ $$ /$$__  $$| $$|_  $$_/   /$$__  $$| $$  | $$ /$$__  $$      |  $$$$$$  /$$_____/ /$$__  $$| $$ /$$__  $$|_  $$_/  
| $$$$_  $$$$| $$  \__/| $$  | $$    | $$$$$$$$| $$  | $$| $$  \ $$       \____  $$| $$      | $$  \__/| $$| $$  \ $$  | $$    
| $$$/ \  $$$| $$      | $$  | $$ /$$| $$_____/| $$  | $$| $$  | $$       /$$  \ $$| $$      | $$      | $$| $$  | $$  | $$ /$$
| $$/   \  $$| $$      | $$  |  $$$$/|  $$$$$$$|  $$$$$$/| $$$$$$$/      |  $$$$$$/|  $$$$$$$| $$      | $$| $$$$$$$/  |  $$$$/
|__/     \__/|__/      |__/   \___/   \_______/ \______/ | $$____/        \______/  \_______/|__/      |__/| $$____/    \___/  
                                                         | $$                                              | $$                
                                                         | $$                                              | $$                
                                                         |__/                                              |__/                

                   Developed By Mahbodfl
                   WriteUp Script
{Fore.MAGENTA}''')


# Read the settings file
with open("data/config.json", "r") as config_file:
    config = json.load(config_file)

# Log settings
def logger():
    logging.basicConfig(filename='information/info.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger()

# Receive and process information from RSS
def get_write_ups(weblog_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(weblog_url, headers=headers)
        response.raise_for_status()
        root = etree.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {weblog_url}: {e}")
        return []
    except etree.XMLSyntaxError as e:
        logging.error(f"Error parsing XML from {weblog_url}: {e}")
        return []

    write_ups = []
    for item in root.findall(".//item"):
        title = item.find("title").text if item.find("title") is not None else "No title"
        link = item.find("guid").text if item.find("guid") is not None else item.find("link").text if item.find("link") is not None else "No link"
        date = item.find("pubDate").text if item.find("pubDate") is not None else "No pubDate"
        write_ups.append([title, link, date])

    return write_ups

# Check and record posts in the database
def check_post(write_ups):
    connection = sqlite3.connect(config["Database"]["FilePath"])
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS "Posts"
                      (
                        id INTEGER PRIMARY KEY,
                        "Title" TEXT NOT NULL,
                        "Link" TEXT NOT NULL,
                        "PubDate" TEXT
                      )''')

    result = 0
    for write_up in write_ups:
        title, link, date = write_up
        cursor.execute('''SELECT * FROM "Posts" WHERE "Title"=? OR "Link"=?''', (title, link))
        if not cursor.fetchone():
            cursor.execute('''INSERT INTO "Posts"("Title", "Link", "PubDate") VALUES (?, ?, ?)''', (title, link, date))
            connection.commit()
            logging.info(f"Added To Database: {title}")
            discord_server(title, link, date)
            telegram_server(title, link, date)
            result += 1
            time.sleep(30)

    connection.close()
    return result

# Send Posts to Discord
def discord_server(title, link, date):
    embed = {
        "title": f"**📢 New Write-up: {title}**",
        "description": f"🗓 **Published on:** {date}\n🔗 [Read more]({link})",
        "color": 7506394,  # Hex color code (0x72A0C1)
        "thumbnail": {"url": "https://media.tenor.com/ju5hhb03JgIAAAAC/dark.gif"},
        "footer": {
        "text": ":ninja: Write-up  \nGIthub: https://github.com/M-thefl\nsupport : https://discord.gg/PNJaQabHJZ",
        }
    }

    body = {
        "username": "fl",
        "avatar_url": "https://avatars.githubusercontent.com/u/123509083?s=400&u=06ebbd267c34d61e4f109e2ba503875473cb101c&v=4",
        "embeds": [embed]
    }
    
    try:
        req = requests.post(config["Discord"]["WebHook"], json=body)
        req.raise_for_status()
        logging.info(f"Added To Discord: {title}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error posting to Discord: {e}")

# Send Posts to Telegram
def telegram_server(title, link, date):
    text = f"📢 *New Write-up: {title}*\n🗓 *Published on:* {date}\n🔗 [Read more]({link})"
    url = f"https://api.telegram.org/bot{config['Telegram']['BotToken']}/sendMessage"
    payload = {
        "chat_id": config["Telegram"]["ChatID"],
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        req = requests.post(url, json=payload)
        req.raise_for_status()
        logging.info(f"Added To Telegram: {title}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error posting to Telegram: {e}")

# Main function
def main():
    while True:
        for tag_url in config.get("TagURLs", []):
            logging.info(f"Check: {tag_url}")
            write_ups = get_write_ups(tag_url)
            result = check_post(write_ups)
            if result != 0:
                logging.info(f"{result} New Writeup.")
                time.sleep(5)

        logging.info("No New Writeups Available.")
        time.sleep(50)

if __name__ == "__main__":
    main()