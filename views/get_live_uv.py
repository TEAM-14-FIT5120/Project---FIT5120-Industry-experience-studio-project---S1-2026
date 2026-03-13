import streamlit as st
import requests
from streamlit_js_eval import get_geolocation


st.title("Live UV & Temperature Monitor")
user_location = get_geolocation()
def get_weather_data(user_location):


    if user_location:
        lat = user_location['coords']['latitude']
        lon = user_location['coords']['longitude']
        api_key = st.secrets["api_keys"]["openweather"]

        exclude = "minutely,hourly,daily,alerts"
        uv_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(uv_url).json()
            if "current" in response:
                return response["current"]
        except Exception as e:
            st.error(f"API Error: {e}")
            
            
    return None


    

