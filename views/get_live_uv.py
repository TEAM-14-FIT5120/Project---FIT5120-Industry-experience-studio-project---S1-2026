import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime


def reverse_geocode_location(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "jsonv2",
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "uvsense_app"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        address = data.get("address", {})

        suburb = (
            address.get("suburb")
            or address.get("city_district")
            or address.get("neighbourhood")
            or address.get("quarter")
            or address.get("town")
            or address.get("city")
            or address.get("village")
            or "Current Location"
        )

        state = address.get("state", "")
        country = address.get("country", "Australia")

        state_map = {
            "Victoria": "VIC",
            "New South Wales": "NSW",
            "Queensland": "QLD",
            "South Australia": "SA",
            "Western Australia": "WA",
            "Tasmania": "TAS",
            "Northern Territory": "NT",
            "Australian Capital Territory": "ACT"
        }

        state_abbr = state_map.get(state, state)

        if suburb and state_abbr:
            return f"{suburb}, {state_abbr}"

        if suburb and country:
            return f"{suburb}, {country}"

        return "Current Location"

    except Exception:
        return "Melbourne, VIC"


def get_browser_location():
    if "browser_location" not in st.session_state:
        st.session_state["browser_location"] = None
    if "location_attempted" not in st.session_state:
        st.session_state["location_attempted"] = False

    if st.session_state["browser_location"] is None and not st.session_state["location_attempted"]:
        result = streamlit_js_eval(
            js_expressions="""
            new Promise((resolve) => {
                if (!navigator.geolocation) {
                    resolve({
                        success: false,
                        error_message: "Geolocation is not supported by this browser."
                    });
                    return;
                }

                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve({
                            success: true,
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            accuracy: position.coords.accuracy
                        });
                    },
                    (error) => {
                        resolve({
                            success: false,
                            error_message: error.message
                        });
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            })
            """,
            key="auto_geo_js"
        )

        if result is not None:
            st.session_state["browser_location"] = result
            st.session_state["location_attempted"] = True

    return st.session_state["browser_location"]


def geocode_location(query):
    api_key = st.secrets["api_keys"]["openweather"]
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": query,
        "limit": 1,
        "appid": api_key
    }

    try:
        response = requests.get(geo_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            place = data[0]

            state = place.get("state", "")
            state_map = {
                "Victoria": "VIC",
                "New South Wales": "NSW",
                "Queensland": "QLD",
                "South Australia": "SA",
                "Western Australia": "WA",
                "Tasmania": "TAS",
                "Northern Territory": "NT",
                "Australian Capital Territory": "ACT"
            }
            state_abbr = state_map.get(state, state)

            return {
                "name": place.get("name"),
                "state": state_abbr,
                "country": place.get("country", ""),
                "lat": place.get("lat"),
                "lon": place.get("lon")
            }

        return None

    except Exception:
        return None


def get_weather_data(location_query=None):
    lat = -37.8136
    lon = 144.9631
    used_default_location = True
    location_error = None
    display_location = "Melbourne, VIC"

    # 1. Search overrides auto-location
    if location_query:
        place = geocode_location(location_query)

        if place and place.get("lat") is not None and place.get("lon") is not None:
            lat = place["lat"]
            lon = place["lon"]
            used_default_location = False

            if place.get("name") and place.get("state"):
                display_location = f"{place['name']}, {place['state']}"
            elif place.get("name") and place.get("country"):
                display_location = f"{place['name']}, {place['country']}"
            else:
                display_location = place.get("name", "Selected Location")
        else:
            location_error = "Location not found"

    # 2. If no search, use browser location
    else:
        location = get_browser_location()

        if location and isinstance(location, dict):
            if location.get("success") is True:
                lat = location.get("latitude", lat)
                lon = location.get("longitude", lon)
                used_default_location = False
                display_location = reverse_geocode_location(lat, lon)
            else:
                location_error = location.get("error_message", "Location access failed.")

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
            data["used_default_location"] = used_default_location
            data["location_error"] = location_error
            data["display_location"] = display_location
            return data
        return None

    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def get_uv_protection_window(weather_data):
    if not weather_data or "hourly" not in weather_data:
        return None, None

    high_uv_hours = [
        hour for hour in weather_data["hourly"][:24]
        if hour.get("uvi", 0) >= 3
    ]

    if not high_uv_hours:
        return "No protection required today", ""

    start_ts = high_uv_hours[0]["dt"]
    end_ts = high_uv_hours[-1]["dt"]

    timezone_offset = weather_data.get("timezone_offset", 0)

    start_time = datetime.fromtimestamp(start_ts + timezone_offset).strftime("%I:%M %p").lstrip("0")
    end_time = datetime.fromtimestamp(end_ts + timezone_offset).strftime("%I:%M %p").lstrip("0")

    return start_time, end_time