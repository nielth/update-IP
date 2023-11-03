import requests
import os
import json
import time

from sys import exit
from pathlib import Path
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

load_dotenv()

fle = Path('ip.txt')
fle.touch(exist_ok=True)

WEBHOOK_DISCORD = os.getenv('WEBHOOK')

DOMAIN_TOKEN = os.getenv('TOKEN')
DOMAIN_SECRET = os.getenv('SECRET')
DOMAINID = os.getenv('DOMAINID')
RECORDID = os.getenv('RECORDID')

URL = "https://httpbin.org/ip"

put_domain = {
    "data": "",
    "host": "@",
    "ttl": 3600,
    "type": "A"
}

def discordMsg(msg=""):
    webhook = DiscordWebhook(url=WEBHOOK_DISCORD, content=msg)
    try:
        webhook.execute()
    except Exception as e:
        print("Could not post message to Discord")


tries = 0

while True:
    with open("ip.txt", "r+") as file:
        ip_addr = file.read()
        file.seek(0)
        try:
            r = requests.get(url=URL)
            tries = 0
        except Exception as e:
            if tries >= 10:
                discordMsg('Could not retrieve public IP')
                print("Could not retrieve public IP")
                time.sleep(60*5)
            tries += 1
            continue
        data = r.json()
        put_domain.update({"data": data['origin']})
        file.write(data['origin'])
        file.truncate()
        if data['origin'] != ip_addr:
            print("Updating IP address on domeneshop...")
            try:
                r = requests.put(f'https://{DOMAIN_TOKEN}:{DOMAIN_SECRET}@api.domeneshop.no/v0/domains/{DOMAINID}/dns/{RECORDID}', timeout=10, data=json.dumps(put_domain))
                if r.status_code != 204:
                    discordMsg('Could not update IP')
                    print("Could not update IP")
                    time.sleep(60*60*24)
                    continue
                print("Successfully updated IP address!")
                discordMsg(f'Server IP: {data["origin"]}')
            except Exception as e:
                discordMsg('Could not update IP')
                print("Could not update IP")
                time.sleep(60*60*24)
                continue

        time.sleep(60)
