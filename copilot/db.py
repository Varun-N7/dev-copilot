import os
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URI"])
db = client[os.environ.get("MONGO_DB_NAME", "devcopilot")]
embeddings_col = db["embeddings"]