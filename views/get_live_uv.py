import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime



st.title("Live UV & Temperature Monitor")

def get_weather_data():
    location = get_geolocation()

    if location:
        lat = location['coords']['latitude']
        lon = location['coords']['longitude']
        api_key = st.secrets["api_keys"]["openweather"]

        exclude = "minutely,daily,alerts"
        uv_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(uv_url).json()
            if "current" in response:
                return response
        except Exception as e:
            st.error(f"API Error: {e}")
    return None

def get_uv_protection_window(weather_data):
    if not weather_data or 'hourly' not in weather_data:
        return None, None

    # Filter hours in the next 24h where UVI is 3 or higher
    high_uv_hours = [hour for hour in weather_data['hourly'][:24] if hour.get('uvi', 0) >= 3]

    if not high_uv_hours:
        return "No protection required today", None

    # Get the start of the first hour and the end of the last hour
    start_ts = high_uv_hours[0]['dt']
    end_ts = high_uv_hours[-1]['dt']

    start_time = datetime.fromtimestamp(start_ts).strftime('%-I:%M %p')
    end_time = datetime.fromtimestamp(end_ts).strftime('%-I:%M %p')

    return start_time, end_time
    

