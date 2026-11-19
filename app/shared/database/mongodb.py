from pymongo import AsyncMongoClient
from app.config import settings

client: AsyncMongoClient | None = None


async def connect_to_mongodb():
    global client

    client = AsyncMongoClient(settings.MONGODB_URL)

    # Verify the database connection
    await client.admin.command("ping")

    print("MongoDB connected successfully!")


async def close_mongodb_connection():
    global client

    if client is not None:
        await client.close()
        client = None
        print("MongoDB connection closed.")


def get_database():
    if client is None:
        raise RuntimeError("MongoDB is not connected")

    return client[settings.DATABASE_NAME]


async def check_database_connection():
    if client is None:
        return False

    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False