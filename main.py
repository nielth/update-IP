import requests
import os

from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()

fle = Path('ip.txt')
fle.touch(exist_ok=True)

WEBHOOK_DISCORD = os.getenv('WEBHOOK')
URL = "https://api.ipify.org/?format=json"

with open("ip.txt", "r+") as file:
    ip_addr = file.read()
    file.seek(0)
    r = requests.get(url=URL)
    data = r.json()
    print(data['ip'])
    print(ip_addr)
    file.write(data['ip'])
    file.truncate()
    if data['ip'] != ip_addr:
        webhook = DiscordWebhook(url=WEBHOOK_DISCORD, content=f"Server IP: {data['ip']}")
        response = webhook.execute()