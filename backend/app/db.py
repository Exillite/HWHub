from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from settings import MONGODB_URL, MONGODB


# Warning
class DataBase:
    client: AsyncIOMotorClient = None  # type: ignore
    db: AsyncIOMotorDatabase = None  # type: ignore


db = DataBase()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(f"{MONGODB_URL}")
    db.db = db.client[MONGODB]


async def close_mongo_connection():
    db.client.close()
