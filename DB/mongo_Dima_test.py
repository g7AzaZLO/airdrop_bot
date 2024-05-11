from pymongo import MongoClient
import pymongo
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    # MongoDB connection URI
    uri = "mongodb+srv://xDShiro:Serfcxd1@clustertest.rthbolv.mongodb.net"
    # Create a client instance
    client = AsyncIOMotorClient(uri)
    # Select the database
    db = client.botTest
    # Select the collection
    collection = db.users
    # Data to insert
    user_data = {"name": "Tima", "email": "Tima@example.com"}
    # Asynchronously insert a document
    await collection.insert_one(user_data)
    print("Inserted a document.")
    # Asynchronously find the inserted document
    document = await collection.find_one({"name": "Tima"})
    print(f"Retrieved document: {document}")
    # Fetch all documents in the collection
    cursor = collection.find({})
    async for document in cursor:
        print(document)

    # Asynchronously delete the inserted document
    # await collection.delete_one({"name": "John Doe"})
    # print("Deleted the document.")
    # Close the connection
    client.close()

if __name__ == "__main__":
    asyncio.run(main())