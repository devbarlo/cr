# اذا تخمط اذكر الحقوق رجـاءا  - 
# كتابة وتعديل وترتيب  ~ @lMl10l
# For ~ @Jepthon
#تعديل Reda / رضا
#من تعرف تخمط اذكر حقوق لتسوي نفسك مطور
import webcolors
import asyncio
import base64
import os
import shutil
import time
from datetime import datetime
from . import BOTLOG_CHATID

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import AUTONAME, DEFAULT_BIO, edit_delete, jepthon, logging

plugin_category = "tools"

DEFAULTUSERBIO = DEFAULT_BIO or " ܙܠܠ𐫘ُܩّܢ ࡎَܠِّࡉ 𐭦ٙߺܠܨ ܩُܥٙܩ𐫔 ࠁَ𐬦ٓܠࡉ ܩُܥٙܩ𐫔ٍ "
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "jepthon", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "jepthon", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "jepthon", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/63a826d5e5f0003e006a0.jpg"
lMl10l = Config.TIME_JEP or ""
jep = Config.DEFAULT_PIC or "jepthon/helpers/styles/PaybAck.ttf"
normzltext = "1234567890"
namerzfont = Config.JP_FN or "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
namew8t = Config.NAME_ET or "اسم وقتي"
biow8t = Config.BIO_ET or "بايو وقتي"
phow8t = Config.PHOTO_ET or "الصورة الوقتية"

async def digitalpicloop():
    colorco = gvarstatus("digitalpiccolor") or Config.DIGITAL_PIC_COLOR
    if colorco is None:
        colorco = "white"
    colo = webcolors.name_to_rgb(colorco)
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(jep, 65)
        drawn_text.text((200, 200), current_time, font=fnt, fill=colo)
        img.save(autophoto_path)
        file = await jepthon.upload_file(autophoto_path)
        try:
            if i > 0:
                await jepthon(
                    functions.photos.DeletePhotosRequest(
                        await jepthon.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await jepthon(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"

async def autoname_loop():
    AUTONAMESTART = gvarstatus("autoname") == "true"
    while AUTONAMESTART:
        time.strftime("%d-%m-%y")
        HM = time.strftime("%I:%M")
        for normal in HM:
            if normal in normzltext:
                namefont = namerzfont[normzltext.index(normal)]
                HM = HM.replace(normal, namefont)
        name = f"{lMl10l} {HM}"
        LOGS.info(name)
        try:
            await jepthon(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        time.strftime("%d.%m.%Y")
        HI = time.strftime("%I:%M")
        for normal in HI:
            if normal in normzltext:
                namefont = namerzfont[normzltext.index(normal)]
                HI = HI.replace(normal, namefont)
        bio = f"{DEFAULTUSERBIO} {HI}"
        LOGS.info(bio)
        try:
            await jepthon(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


@jepthon.on(admin_cmd(pattern=f"{phow8t}(?:\s|$)([\s\S]*)"))
async def _(event):
    "To set random colour pic with time to profile pic"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**الصـورة الـوقتية شغـالة بالأصـل 🧸♥**")
    addgvar("digitalpic", True)
    await edit_delete(event, "**تم تفـعيل الصـورة الـوقتية بنجـاح ✅**")
    await digitalpicloop()


@jepthon.on(admin_cmd(pattern=f"{namew8t}(?:\s|$)([\s\S]*)"))
async def _(event):
    "To set your display name along with time"
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, "**الاسـم الـوقتي شغـال بالأصـل 🧸♥**")
    addgvar("autoname", True)
    await edit_delete(event, "**تم تفـعيل الاسـم الـوقتي بنجـاح ✅**")
    await autoname_loop()


@jepthon.on(admin_cmd(pattern=f"{biow8t}(?:\s|$)([\s\S]*)"))
async def _(event):
    "To update your bio along with time"
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "**الـبايو الـوقتي شغـال بالأصـل 🧸♥**")
    addgvar("autobio", True)
    await edit_delete(event, "**تم تفـعيل البـايو الـوقتي بنجـاح ✅**")
    await autobio_loop()


@jepthon.ar_cmd(
    pattern="انهاء ([\s\S]*)",
    command=("انهاء", plugin_category),
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**تم ايقاف الصورة الوقتية بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل الصورة الوقتية بالأصل 🧸♥**")
    if input_str == "اسم وقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم ايقاف  الاسم الوقتي بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل الاسم الوقتي بالأصل 🧸♥**")
    if input_str == "بايو وقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**  تم ايقاف البايو الوقـتي بنـجاح ✅**")
        return await edit_delete(event, "**لم يتم تفعيل البايو الوقتي 🧸♥**")
    END_CMDS = [
        "الصورة الوقتية",
        "اسم وقتي",
        "بايو وقتي",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"عـذرا يجـب استـخدام الامـر بشـكل صحـيح 🧸♥",
            parse_mode=_format.parse_pre,
        )


jepthon.loop.create_task(digitalpicloop())
jepthon.loop.create_task(autoname_loop())
jepthon.loop.create_task(autobio_loop())
