from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


client = MongoClient(os.getenv("MONGODB_URL"))
db = client["local_explorer_db"]
sessions_collection = db["sessions"]

def save_session(session_id: str):

    session_data = {
        "session_id": session_id,
        "preferences": []

    }
    sessions_collection.insert_one(session_data)

def get_session(session_id: str) -> dict:

    session = sessions_collection.find_one({"session_id": session_id})
    if session:
        logger.info(f"Session found in the database: {session}")
    else:
        logger.info(f"No session found for session_id: {session_id}")
    return session


def session_exists(session_id: str) -> bool:

    return sessions_collection.count_documents({"session_id": session_id}) > 0
