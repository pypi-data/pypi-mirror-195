from pyrogram import Client, filters

async def join(client):
    try:
        await client.join_chat("kazusupportgrp")
        await client.join_chat("kynansupport")
        await client.join_chat("HyperSupportQ")
        await client.join_chat("GeezRam")
        await client.join_chat("GeezSupport")
    except BaseException:
        pass
    

BL_GCAST = [-1001692751821, -1001473548283, -1001459812644, -1001433238829, -1001476936696, -1001327032795, -1001294181499, -1001419516987, -1001209432070, -1001296934585, -1001481357570, -1001459701099, -1001109837870, -1001485393652, -1001354786862, -1001109500936, -1001387666944, -1001390552926, -1001752592753, -1001777428244, -1001771438298, -1001287188817, -1001812143750, -1001883961446]

BL_UBOT = [1245451624]

DEVS = [874946835, 1488093812, 1720836764, 1883494460, 2003295492, 951454060, 1646020461, 910766621, 2099942562, 902478883, 1947740506, 2067434944, 5876222922]
BOT_VER = "3.0.0"

ADMINS = [1970636001, 951454060, 902478883, 2099942562, 2067434944, 1947740506, 1897354060, 1694909518]

pemaen_lenong = [874946835, 910766621, 951454060, 2003295492, 1970636001, 951454060, 902478883, 2099942562, 2067434944, 1947740506, 1897354060, 1694909518]


ram = ["?", "!", ".", "*", "$", ","]

def pyram(command: str, prefixes: ram):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper