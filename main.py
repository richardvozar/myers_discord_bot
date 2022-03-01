#!/usr/bin/env python

import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks, commands


URL = 'https://progameguides.com/dead-by-daylight/dead-by-daylight-codes/'
BOT_ONLINE = False

# updated date
old_date_string = ''
new_date_string = ''

load_dotenv()

client = discord.Client()



# updated_string --> str | [Updated Feb. 24]
# codes --> dict | 'CODE': 'Reedem for XX BP'
def get_codes(updated_string, codes):
    ret = '__**Dead by Daylight Reedem Codes:**__ '
    ret += updated_string
    ret += '\n'
    for c, bp in codes.items():
        ret += f'*{c}* --> {bp}\n'
    return ret


@client.event
async def on_ready():
    global BOT_ONLINE
    print(f'{client.user} is now online!')
    BOT_ONLINE = True



@tasks.loop(seconds=600)
async def code_update():
    global BOT_ONLINE, old_date_string, new_date_string

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main')

    updated_selector = soup.select('div p strong')
    updated_string = str(updated_selector.pop().get_text())

    # changing the updates
    old_date_string, new_date_string = new_date_string, updated_string

    codes_src = soup.select('#dbd-codes-working + ul li')

    codes_src = list(codes_src)

    codes = {}
    for c_src in codes_src:
        txt = str(c_src.get_text()).split('—')
        codes[txt[0]] = txt[1]

    if BOT_ONLINE:
        channel = client.get_channel(947922114516766741)

        if old_date_string == '':
            old_date_string = updated_string
            await channel.send(get_codes(updated_string, codes))

        if old_date_string == new_date_string:
            return
        else:
            await channel.send(get_codes(updated_string, codes))



code_update.start()
client.run(os.getenv('TOKEN'))


