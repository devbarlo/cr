# Copyright 2021 TerminalWarlord under the terms of the MIT
# license found at https://github.com/TerminalWarlord/TikTok-Downloader-Bot/blob/master/LICENSE
# Encoding = 'utf-8'
#Edited by Reda
import asyncio 
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from jepthon import jepthon 
#from ..Config import Config

@jepthon.ar_cmd(func=lambda m:'reda')
async def tiktok_dl(message):
    ms = message.text
    #await jepthon.send_message("@WKKKN", f"{message.sender}")
    if message.sender is None or message.sender.id == Config.OWNER_ID or message.sender.id in Config.SUDO_USERS:

        if ".تك https://vm.tiktok.com/" in ms:
            await message.delete()
            a = await jepthon.send_message(message.chat.id, 'يجري البحث عن الملف..', parse_mode='md')
            link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
            link = link.split("?")[0]



    
            params = {
              "link": link
            }
            headers = {
              'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
              'x-rapidapi-key': "f9d65af755msh3c8cac23b52a5eep108a33jsnbf7de971bb72"
            }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment 
    
            api = f"https://tiktok-info.p.rapidapi.com/dl/"
            r = requests.get(api, params=params, headers=headers).json()['videoLinks']['download']
            directory = str(round(time.time()))
            filename = str(int(time.time()))+'.mp4'
            #size = int(requests.head(r).headers['Content-Length'])
            is_chunked = requests.head(r).headers.get('transfer-encoding', '')
            content_length_s = requests.head(r).headers.get('content-length')
            if not is_chunked and content_length_s.isdigit():
                size = int(content_length_s)
            else:
                size = None
            total_size = "{:.2f}".format(int(size) / 1048576)
            try:
                os.mkdir(directory)
            except:
                pass
            with requests.get(r, timeout=(50, 10000), stream=True) as r:
                r.raise_for_status()
                with open(f'./{directory}/{filename}', 'wb') as f:
                    chunk_size = 1048576
                    dl = 0
                    show = 1
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        dl = dl + chunk_size
                        percent = round(dl * 100 / size)
                        if percent > 100:
                            percent = 100
                        if show == 1:
                            try:
                                await a.edit(f'__**URL :**__ __{message.text}__\n'
                                f'__**Total Size :**__ __{total_size} MB__\n'
                                f'__**Downloaded :**__ __{percent}%__\n',
                                disable_web_preview=False)
                            except:
                                pass
                        if percent == 100:
                            show = 0

            await a.edit(f' يجري التحميل للخادم..!\n'
               f' يجري الرفع للتلجرام⏳__')
            start = time.time()
            title = filename
            catid = await reply_id(message)
            await message.client.send_file(
               message.chat_id, f"./{directory}/{filename}", reply_to=catid, force_document=True, parse_mode='md', caption=f"**الملف : ** {filename}\n**الحجم :** {total_size} MB"
             )
        
            await a.delete()
     
            shutil.rmtree(directory)
    else:
        return None
