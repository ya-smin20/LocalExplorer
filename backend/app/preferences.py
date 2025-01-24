from app.db import sessions_collection
from bson.objectid import ObjectId
import logging

logger = logging.getLogger("app.preferences")

def initialize_preferences(session_id: str) -> None:

    sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"preferences": []}},
        upsert=True
    )
    logger.info(f"Preferences initialized for session: {session_id}")


def add_preference(session_id: str, preference: str) -> None:
    logger.info(f"Attempting to add preference: {preference} for session: {session_id}")
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$addToSet": {"preferences": preference}}
    )
    logger.info(f"Preference '{preference}' added for session: {session_id}")



def get_preferences(session_id: str) -> list:

    session = sessions_collection.find_one({"session_id": session_id}, {"preferences": 1})
    return session.get("preferences", []) if session else []


def remove_preference(session_id: str, preference: str) -> None:

    
    result = sessions_collection.update_one(
        {"session_id": session_id},
        {"$pull": {"preferences": preference}}
    )

  
    if result.matched_count == 0:
        logger.warning(f"No session found for session_id: {session_id}. No changes made.")
    elif result.modified_count == 0:
        logger.warning(f"Preference '{preference}' not found in preferences for session: {session_id}.")
    else:
        logger.info(f"Preference '{preference}' removed for session: {session_id}")

