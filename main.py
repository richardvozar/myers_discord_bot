#!/usr/bin/env python

import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks, commands
from datetime import datetime as dt



URL = 'https://progameguides.com/dead-by-daylight/dead-by-daylight-codes/'
BOT_ONLINE = False

# updated date
old_codes = ''
new_codes = ''

load_dotenv()

client = discord.Client()


# cutting the first line of the message
def cut_first_line(msg):
    return msg[msg.index('\n')+1:]


# updated_string --> str | [Updated Feb. 24]
# codes --> dict | 'CODE': 'Reedem for XX BP'
def get_codes(updated_string, codes):
    ret = '**Dead by Daylight Reedem Codes:** ['
    ret += updated_string
    ret += ']\n'
    for c, bp in codes.items():
        ret += f'*{c}* --> {bp}\n'
    return ret


@client.event
async def on_ready():
    global BOT_ONLINE
    print(f'{client.user} is now online!')
    BOT_ONLINE = True




@tasks.loop(seconds=10)
async def code_update():
    global BOT_ONLINE, old_codes, new_codes

    dbd_codes_channel = client.get_channel(947922114516766741)

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main')

    updated_selector = soup.select('div p strong')
    updated_string = str(updated_selector.pop().get_text())


    codes_src = soup.select('#dbd-codes-working + ul li')

    codes_src = list(codes_src)


    if BOT_ONLINE:

        last_msg_list = await dbd_codes_channel.history(limit=1).flatten()
        last_msg = last_msg_list[0].content
        #print(cut_first_line(last_msg))




        # putting codes in the dictionary 'codes'
        codes = {}
        for c_src in codes_src:
            txt = str(c_src.get_text()).split('—')
            codes[txt[0]] = txt[1]

        # changing the updates
        old_codes = new_codes
        #print(f'old_codes={old_codes}  <--')

        # copying key-value pairs from codes, to new_codes
        new_codes = {}
        for k, v in codes.items():
            new_codes[k] = v


        channel = client.get_channel(947922114516766741)

        if old_codes == '':
            #print('old_codes=""', old_codes, new_codes)
            date = dt.now().strftime('%Y. %b %m. %X')
            print('-- log: FIRST RUN: ' + date)


            #print(len(cut_first_line(last_msg)), len(cut_first_line(get_codes(date, codes))))



            if abs(len(cut_first_line(last_msg)) - len(cut_first_line(get_codes(date, codes)))) < 5:
                return
            else:
                await channel.send(get_codes(date, codes))

        elif old_codes == new_codes:
            #print('old_codes == new_codes', old_codes, new_codes)
            return

        else:
            #print('wut')
            date = dt.now().strftime('%Y. %b %m. %X')
            print('-- log: NEW CODE: ' + date)


            if abs(len(cut_first_line(last_msg)) - len(cut_first_line(get_codes(date, codes)))) < 5:
                return
            else:
                await channel.send(get_codes(date, codes))



code_update.start()
client.run(os.getenv('TOKEN'))


