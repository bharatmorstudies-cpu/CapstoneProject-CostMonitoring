import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db_client():
    """Initializes and returns a reusable MongoDB client instance connection."""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://root:SecureMongoPassword123@localhost:27017/devops_metrics?authSource=admin")
    try:
        client = MongoClient(mongo_uri)
        # Force a connection test to ping the deployment cluster node boundary
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"❌ Failed to instantiate connection pooling matrix to MongoDB cluster: {str(e)}")
        raise e

def get_collection(collection_name: str = "cloud_costs"):
    """Retrieves the targeted metrics context tracking collection context layer."""
    client = get_db_client()
    db = client["devops_metrics"]
    return db[collection_name]
