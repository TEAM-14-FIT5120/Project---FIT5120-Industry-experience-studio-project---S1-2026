import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
import plotly.graph_objects as go


st.title("Live UV & Temperature Monitor")

def get_weather_data():
    location = get_geolocation()

    if location:
        lat = location['coords']['latitude']
        lon = location['coords']['longitude']
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
    

