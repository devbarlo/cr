import os.path
from jepthon import jepthon
from ..core.managers import edit_delete, edit_or_reply
#By Reda
def isEx(path):
     spath = str(path)
     return os.path.exists(f"jepthon/plugins/{spath}.py")

@jepthon.ar_cmd(pattern="موجود؟(?:\s|$)([\s\S]*)")

async def _(event):
    input_str = event.pattern_match.group(1)
    re = isEx(str(input_str))
    return await edit_or_reply(event, str(re))
