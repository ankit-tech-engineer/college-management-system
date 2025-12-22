from config.database import get_db

async def get_next_sequence(name: str) -> int:
    db = await get_db()
    counter = await db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]