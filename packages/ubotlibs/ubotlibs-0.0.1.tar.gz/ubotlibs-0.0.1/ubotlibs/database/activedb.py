from pyrogram.filters import chat
from . import cli
from typing import Dict, List, Union
from datetime import datetime, timedelta

collection = cli["Kyran"]["active"]



async def get_active_time(user_id):
    expire_date = await get_expired_date(user_id)
    if expire_date:
        active_time = expire_date - datetime.now()
        return active_time
    else:
        return None

async def get_expired_date(user_id):
    user = await collection.users.find_one({'_id': user_id})
    if user:
        return user.get('expire_date')
    else:
        return None

def set_expired_date(user_id, expire_date):
    collection.users.update_one({'_id': user_id}, {'$set': {'expire_date': expire_date}}, upsert=True)



async def rem_expired_date(user_id):
    await collection.users.update_one(
        {"_id": user_id}, {"$unset": {"expire_date": ""}}, upsert=True
    )
