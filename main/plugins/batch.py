#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Hem genel hem de özel kanallar için eklenti!
"""

import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import check, get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub

ft = f"Bu botu kullanmak için katılmanız gerekiyor @{fs}."

batch = []

async def get_pvt_content(event, chat, id):
    msg = await userbot.get_messages(chat, ids=id)
    await event.client.send_message(event.chat_id, msg) 
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/dl'))
async def _batch(event):
    if not event.is_private:
        return
    # wtf is the use of fsub here if the command is meant for the owner? 
    # well am too lazy to clean 
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if f'{event.sender_id}' in batch:
        return await event.reply("Zaten bir partiye başladın, onun tamamlamasını bekle")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("Bu mesaja yanıt olarak, kaydetmeye başlamak istediğiniz mesaj bağlantısını bana gönderin.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("Bağlantı bulunamadı.")
            except Exception as e:
                print(e)
                return await conv.send_message("Yanıtınız için daha fazla bekleyemezsiniz!")
            await conv.send_message("Bu mesaja cevap olarak bana verilen mesajdan kaydetmek istediğiniz dosya sayısını/aralığı gönderin.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                return await conv.send_message("Yanıtınız için daha fazla bekleyemezsiniz!")
            try:
                value = int(_range.text)
                if value > 100:
                    return await conv.send_message("Tek bir toplu işte en fazla 100 dosya alabilirsiniz")
            except ValueError:
                return await conv.send_message("Aralık bir tamsayı olmalıdır!")
            s, r = await check(userbot, Bot, _link)
            if s != True:
                await conv.send_message(r)
                return
            batch.append(f'{event.sender_id}')
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.pop(0)
            
            
async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 6
        if i < 50 and i > 25:
            timer = 10
        if i < 100 and i > 50:
            timer = 15
        if not 't.me/c/' in link:
            if i < 25:
                timer = 5
            else:
                timer = 6
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            fw_alert = await client.send_message(sender, f"Floodwait nedeniyle f'{fw.x} saniye uyuyor.")
            await asyncio.sleep(fw.x + 5)
            await fw_alert.delete()
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"Floodwaits ve Protect hesabından kaçınmak için `{timer}` saniye uykuda!")
        time.sleep(timer)
        await protection.delete()
            
                

