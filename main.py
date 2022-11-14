import requests
import os
import json

from sys import exit
from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()

fle = Path('ip.txt')
fle.touch(exist_ok=True)

WEBHOOK_DISCORD = os.getenv('WEBHOOK')

DOMAIN_TOKEN = os.getenv('TOKEN')
DOMAIN_SECRET = os.getenv('SECRET')
DOMAINID = os.getenv('DOMAINID')
RECORDID = os.getenv('RECORDID')

URL = "https://api.ipify.org/?format=json"

put_domain = {
    "data": "",
    "host": "@",
    "ttl": 3600,
    "type": "A"
}

with open("ip.txt", "r+") as file:
    ip_addr = file.read()
    file.seek(0)
    r = requests.get(url=URL)
    if r.status_code != 200:
        exit(1)
    data = r.json()
    put_domain.update({"data": data['ip']})
    file.write(data['ip'])
    file.truncate()
    if data['ip'] != ip_addr:
        webhook = DiscordWebhook(url=WEBHOOK_DISCORD, content=f"Server IP: {data['ip']}")
        response = webhook.execute()
        r = requests.put(f'https://{DOMAIN_TOKEN}:{DOMAIN_SECRET}@api.domeneshop.no/v0/domains/{DOMAINID}/dns/{RECORDID}', data=json.dumps(put_domain))