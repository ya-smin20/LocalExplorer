from dotenv import load_dotenv
import openai
import os
import logging
from app.preferences import get_preferences


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_activity_suggestions(weather_data, time_of_day, nearby_places, session_id):

    try:
        
        user_preferences = get_preferences(session_id)

       
        preferences_text = (
            f"The user prefers activities related to: {', '.join(user_preferences)}."
            if user_preferences else
            "The user has no specific preferences."
        )
       
        prompt = f"""
        The user has a set of preferred activities. The suggested activities should take into account those preferences but should **never repeat** any activities that were previously suggested.
        Suggest a set of fresh and personalized activities based on the following details:
        - Weather: {weather_data['weather'][0]['description']}
        - Temperature: {weather_data['main']['temp']}°C
        - Time of day: {time_of_day}
        - User Preferences: {preferences_text}

        The activities should be dynamic and offer **new** ideas each time, inspired by the user's preferences, but ensuring that the suggestions are **not identical** to previous ones. 

        Please provide:
        - 4 Indoor activities that can be done at home (ensure they are varied and **distinct** from prior suggestions).
        - 4 Outdoor activities suitable for the weather and time, utilizing nearby places with their coordinates and maps:
        {nearby_places}

        The activities should be categorized as follows:
        - **Indoor Activities:**
        List 4 indoor activities that are distinct from previous suggestions.

        - **Outdoor Activities:**
        For each outdoor activity:
        - Provide the name of the place.
        - A short description of the activity.
        - A Google Maps link to the location.

        Ensure the activities are fresh, diverse, and **never repeated**. Output the activities in the following format:

        **Indoor Activities:**
        - Activity: [Activity description]
        
        **Outdoor Activities:**
        - Activity: [Activity description]
        - Place: [Place name]
        - Map: [Google Maps link]
        """

        
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "system", "content": "You are an assistant that provides activity suggestions based on weather, time, and user preferences."},
                      {"role": "user", "content": prompt}],
            max_tokens=350  
        )

        
        activity_suggestions_text = response['choices'][0]['message']['content']
        logger.info(f"Generated activity suggestions: {activity_suggestions_text}")

       
        indoor_activities = []
        outdoor_activities = []
        
        
        activities = activity_suggestions_text.split("\n")
        logger.info(f"Split activities list: {activities}")

        current_category = None

        temp_block = []

        for line in activities:
            line = line.strip()  

           
            if "**Indoor Activities:**" in line:
                if temp_block and current_category == "outdoor":
                    outdoor_activities.append("\n".join(temp_block).strip())
                elif temp_block and current_category == "indoor":
                    indoor_activities.append("\n".join(temp_block).strip())
                current_category = "indoor"
                temp_block = []
                continue

            elif "**Outdoor Activities:**" in line:
                if temp_block and current_category == "indoor":
                    indoor_activities.append("\n".join(temp_block).strip())
                elif temp_block and current_category == "outdoor":
                    outdoor_activities.append("\n".join(temp_block).strip())
                current_category = "outdoor"
                temp_block = []
                continue

         
            if current_category:
                temp_block.append(line)

      
        if temp_block and current_category == "indoor":
            indoor_activities.append("\n".join(temp_block).strip())
        elif temp_block and current_category == "outdoor":
            outdoor_activities.append("\n".join(temp_block).strip())



        return {
            "indoor": indoor_activities,
            "outdoor": outdoor_activities
        }

    except openai.OpenAIError as e:  
        logger.error(f"Error communicating with OpenAI API: {e}")
        return "Sorry, I couldn't generate activity suggestions at the moment."