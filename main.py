#!/usr/bin/env python

import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup



URL = 'https://progameguides.com/dead-by-daylight/dead-by-daylight-codes/'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='main')


updated_selector = soup.select('div p strong')
updated_string = str(updated_selector.pop().get_text())
print(updated_string)


codes_src = soup.select('#dbd-codes-working + ul li')

codes_src = list(codes_src)

codes = {}
for c_src in codes_src:

    txt = str(c_src.get_text()).split('—')

    codes[txt[0]] = txt[1]

print(codes)


# updated_string --> str | [Updated Feb. 24]
# codes --> dict | 'CODE': 'Reedem for XX BP'





load_dotenv()

# instantiate discord client
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} is now online!')

client.run(os.getenv('TOKEN'))


@client.event
async def on_message(message):
    # make sure bot doesn't respond to it's own messages to avoid infinite loop
    if message.author == client.user:
        return

    # lower case message
    message_content = message.content.lower()

    if message.content.startswith(f'$hello'):
        await message.channel.send('''Hello there! I\'m the fidgeting bot from RunPee. 
    Sorry but I really need to go to the bathroom... Please read my manual by typing $help or $commands while I'm away.''')


