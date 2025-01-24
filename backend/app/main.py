import datetime 
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import requests
import logging
from app.activity_suggestions import get_activity_suggestions
from app.nearby import fetch_nearby_places
from app.weather import fetch_weather
from app.session_handling import (
    get_session_cookie,
    validate_session,
    create_new_session
)
from app.db import get_session, save_session
from app.preferences import initialize_preferences
from app.routes.preferences_routes import router as preferences_router

load_dotenv()

app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.include_router(preferences_router)


app.mount("/static", StaticFiles(directory="../frontend"), name="static")

app.include_router(preferences_router, prefix="/api", tags=["Preferences"])

class Location(BaseModel):
    latitude: float
    longitude: float

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        
        with open(os.path.join("../frontend", "index.html"), "r") as file:
            combined_html = file.read()
        return HTMLResponse(content=combined_html)
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        raise HTTPException(status_code=500, detail="Could not load index.html")





@app.post("/weather")
def get_weather(location: Location, request: Request):
    logger.info(f"User's location - Latitude: {location.latitude}, Longitude: {location.longitude}")
   
    weather_data = fetch_weather(location.latitude, location.longitude)
    
    current_time = datetime.datetime.now().strftime("%I:%M %p")  

    logger.info(f"time: {datetime.datetime.now()}")

  
    nearby_places = fetch_nearby_places(location.latitude, location.longitude)

  
    session_id = request.state.session_id
    

    activity_suggestions = get_activity_suggestions(weather_data, current_time, nearby_places, session_id)

  
    return {
        "weather": weather_data,
        "activity_suggestions": activity_suggestions,
        "nearby_places": nearby_places,

    }



@app.middleware("http")
async def session_middleware(request: Request, call_next):
  
    response = Response()


    session_id = get_session_cookie(request)
  

    if session_id:
      
        session = get_session(session_id)
        if session:
            logger.info(f"Valid session found for session ID: {session_id}")
        else:
          
      
            save_session(session_id)  
            initialize_preferences(session_id)
    else:
       
        session_id = create_new_session(response)

    request.state.session_id = session_id

  
    response = await call_next(request)
    return response


@app.get("/check-session")
async def check_session(request: Request):
    """Endpoint to check the current session ID."""
    return {"session_id": request.state.session_id}

