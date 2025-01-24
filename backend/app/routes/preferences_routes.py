from fastapi import APIRouter, Request
from app.preferences import add_preference, get_preferences, remove_preference

router = APIRouter()

@router.post("/preferences/add")
async def add_user_preference(request: Request):

    preference = request.query_params.get('preference')

    session_id = request.state.session_id
    if not preference:
        return {"error": "Preference is required."}
    add_preference(session_id, preference)
    return {"message": f"Preference '{preference}' added successfully."}

@router.post("/preferences/remove")
async def remove_user_preference(request: Request):
    try:
        data = await request.json()
        print(f"Received data: {data}")  
        preference = data.get("preference")  
        session_id = request.state.session_id

        if not preference:
            return {"error": "Preference is required."}

        remove_preference(session_id, preference)  
        return {"message": f"Preference '{preference}' removed successfully."}
    except Exception as e:

        return {"error": "Failed to remove preference. Please check the request format."}



@router.get("/preferences")
async def get_user_preferences(request: Request):

    session_id = request.state.session_id
    preferences = get_preferences(session_id)
    return {"preferences": preferences}
