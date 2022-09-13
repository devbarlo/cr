"""
Jepthon team ©
By Reda
sub Hussein
"""
import os
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment

from jepthon import jepthon
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type

plugin_category = "utils"


@jepthon.ar_cmd(pattern="احجي(?:\s|$)([\s\S]*)",
               command=("احجي", plugin_category),
              )
async def _(event):
    "تحويل الكلام الى نص."
    
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    lan = input_str
    if not lan:
         return await edit_delete(event, "يجب ان تضع اختصار اللغة المطلوبة")
    
    #ted = await edit_or_reply(event, str(lan))
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    mediatype = media_type(reply)
    if not reply or (mediatype and mediatype not in ["Voice", "Audio"]):
        return await edit_delete(
            event,
            "`قم بالرد على رسالة او مقطع صوتي لتحويله الى نص.`",
        )
    jepevent = await edit_or_reply(event, "`يجري تنزيل الملف...`")
    oggfi = await event.client.download_media(reply, Config.TEMP_DIR)
    await jepevent.edit("`يجري تحويل الكلام الى نص....`")
    r = sr.Recognizer()
    #audio_data = open(required_file_name, "rb").read()
    ogg = oggfi.removesuffix('.ogg')
   
    AudioSegment.from_file(oggfi).export(f"{ogg}.wav", format="wav")
    user_audio_file = sr.AudioFile(f"{ogg}.wav")
    with user_audio_file as source:
         audio = r.record(source)

    
    try:
         text = r.recognize_google(audio, language=str(lan))
    except ValueError:
         return await edit_delete(event, "**لا يوجد كلام في المقطع الصوتي**")
    except BaseException as err:
         return await edit_delete(event, f"**!لا يوجد كلام في هذا المقطع الصوتي\n{err}**")
    end = datetime.now()
    ms = (end - start).seconds
    
    string_to_show = "**يكول : **`{}`".format(
            text
        )
    await jepevent.edit(string_to_show)
    # now, remove the temporary file
    os.remove(oggfi)
    os.remove(f"{ogg}.wav")
