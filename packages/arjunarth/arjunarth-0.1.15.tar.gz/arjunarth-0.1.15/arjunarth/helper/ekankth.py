import os
import sys
from pyrogram import Client

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "BlackWeb"])

async def join(client):
    try:
        await client.join_chat("EkankthProjects")
        await client.join_chat("BlackWebSupport")
    except BaseException:
        pass
