import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import time
import random

PROXIES = []

def getwebstring():
    timenow = datetime.datetime.now()
    stringconv =   "VastidMonitors • Monitors • Kith • "      + timenow.strftime("%X")
    return stringconv

class KithMonitor:

    def __init__(self, proxy_list):

        self.itemList = []
        self.proxy_list = proxy_list
    
        self.addToArray()
        while True:
            self.checkForNew()

    def addToArray(self):


        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }

        while True:

            PROXIES = {
                "http": f"http://{random.choice(self.proxy_list)}",
                "https": f"https://{random.choice(self.proxy_list)}"
            } 
            
            try:

                r = requests.get('https://eu.kith.com/products.json', headers=self.headers, proxies=PROXIES)
            
            except Exception as e:
                print(e)

                print("STATUS: FAILED")
                continue
                
            else:

                productsArray = r.json()['products']

                for items in productsArray:

                    self.itemList.append(items['title'])

                return

    def checkForNew(self):

        itemCount = len(self.itemList)

        while True:

            PROXIES = {
                "http": f"http://{random.choice(self.proxy_list)}",
                "https": f"https://{random.choice(self.proxy_list)}"
            }

            try:

                r = requests.get('https://eu.kith.com/products.json', headers=self.headers, proxies=PROXIES)

            except:

                print("STATUS: FAILED")
                continue

            else:

                productsArray = r.json()['products']

                if len(productsArray) > itemCount:

                    self.foundNewProduct()

                elif len(productsArray) < itemCount:

                    self.itemList = []

                    self.addToArray()

                else:

                    print("SITE MONITORED")

    def foundNewProduct(self):

        while True:

            PROXIES = {
                "http": f"http://{random.choice(self.proxy_list)}",
                "https": f"https://{random.choice(self.proxy_list)}"
            }
            
            try:

                r = requests.get('https://eu.kith.com/products.json', headers=self.headers, proxies=PROXIES)

            except:

                print("STATUS: FAILED")
                continue

            else:

                productsArray = r.json()['products']

                for items in productsArray:

                    if items['title'] not in productsArray:

                        print("NEW ITEM FOUND")
                        self.sendWebook(items['title'], items['variants'][0]['price'], items['images'][0]['src'])
                        #send webhook
                
                return

    def sendWebook(self, itemname, price, image):

        embed = {
            "title": f"**{itemname}**",
            "color": 5814783,
            "footer": {
                "text": getwebstring(),
                "icon_url": "https://pbs.twimg.com/profile_images/1340727732108451840/5T7EMJko_400x400.jpg"
            },
            "fields": [
                {
                "name": "Product Name",
                "value": f"`{itemname}`"
                },
                {
                "name": "Price",
                "value": f"`{price}`"
                }
            ],
            "thumbnail": {
                "url": image
            }
        }

        webhook = DiscordWebhook("https://discord.com/api/webhooks/addwebhookhere", username="VastidMonitors", avatar_url="https://pbs.twimg.com/profile_images/1340727732108451840/5T7EMJko_400x400.jpg")

        webhook.add_embed(embed)

        response = webhook.execute()

def load_proxies():
    with open('proxies.txt') as proxy_file:
        data = proxy_file.read().split()
        for proxy in data:
            host, port, user, password = proxy.split(":")
            PROXIES.append(f"{user}:{password}@{host}:{port}")
    return PROXIES

proxy_list=load_proxies()

KithMonitor(proxy_list)
