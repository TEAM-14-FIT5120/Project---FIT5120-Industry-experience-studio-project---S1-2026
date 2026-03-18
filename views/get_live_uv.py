import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime
from geopy.geocoders import Nominatim


def get_location_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="uvsense_app")
        location = geolocator.reverse((lat, lon), language="en")
        if location and location.raw.get("address"):
            address = location.raw["address"]
            city = (
                address.get("city")
                or address.get("town")
                or address.get("suburb")
                or address.get("village")
                or "Current Location"
            )
            country = address.get("country", "Australia")
            return f"{city}, {country}"
    except Exception:
        pass
    return "Melbourne, Australia"


def get_weather_data():
    location = get_geolocation()

    # Default fallback: Melbourne
    lat = -37.8136
    lon = 144.9631

    if (
        location
        and isinstance(location, dict)
        and "coords" in location
        and location["coords"]
        and "latitude" in location["coords"]
        and "longitude" in location["coords"]
    ):
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]

    api_key = st.secrets["api_keys"]["openweather"]
    exclude = "minutely,daily,alerts"
    uv_url = (
        f"https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(uv_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "current" in data:
            data["display_location"] = get_location_name(lat, lon)
            return data
        return None

    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def get_uv_protection_window(weather_data):
    if not weather_data or 'hourly' not in weather_data:
        return None, None

    high_uv_hours = [
        hour for hour in weather_data['hourly'][:24]
        if hour.get('uvi', 0) >= 3
    ]

    if not high_uv_hours:
        return "No protection required today", ""

    start_ts = high_uv_hours[0]['dt']
    end_ts = high_uv_hours[-1]['dt']

    start_time = datetime.fromtimestamp(start_ts).strftime('%I:%M %p').lstrip('0')
    end_time = datetime.fromtimestamp(end_ts).strftime('%I:%M %p').lstrip('0')

    return start_time, end_time

