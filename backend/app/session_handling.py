import datetime
import uuid
from fastapi import Request, Response
from app.db import save_session, get_session , session_exists

def get_session_cookie(request: Request) -> str:

    session_id = request.cookies.get("session_id")
    if session_id:
        print(f"Session ID retrieved from cookie: {session_id}")
    else:
        print("No session ID found in cookie.")
    return session_id

def create_new_session(response: Response, session_id: str = None) -> str:

    if not session_id:
        session_id = str(uuid.uuid4())  

    if not session_exists(session_id):
        save_session(session_id)  


    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,   
        samesite="Lax", 
        max_age=3600 * 24 * 7, 
        secure=False     
    )
    print(f"New session created: {session_id}")
    return session_id

def validate_session(session_id: str) -> bool:

    session = get_session(session_id)
    if session:
        if session["expires_at"] > datetime.utcnow(): 
            print(f"Session ID {session_id} found in db.")
            return True
        else:
            print(f"Session ID {session_id} has expired.")
    else:
        print(f"Session ID {session_id} not found in the database.")
    return False
