#Github.com/Vasusen-code

import os
from .. import bot as Drone
from telethon import events, Button

from ethon.mystarts import start_srb
    
S = '/' + 's' + 't' + 'a' + 'r' + 't'

@Drone.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Bana bu mesaja yanıt olarak küçük resim için herhangi bir resim gönderin.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("Medya bulunamadı.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("Resim bulunamadı.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Geçici küçük resim kaydedildi!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Deneniyor.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Silindi!')
    except Exception:
        await event.edit("Küçük resim kaydedilmedi.")                        
  
@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    text = "Buraya kopyalamak için herhangi bir ozel kanal mesajın Bağlantısını bana gönder"
    await start_srb(event, text)
    
