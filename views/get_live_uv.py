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


def normalize_query(query):
    """
    Enhance user query with Australian context for better geocoding results.
    """
    q = query.strip()
    q_lower = q.lower()

    # Keep query unchanged if Australia is already specified
    if "australia" in q_lower or ",au" in q_lower or ", au" in q_lower:
        return q

    # If Melbourne is mentioned, strongly bias to Victoria, AU
    if "melbourne" in q_lower:
        return f"{q}, Victoria, AU"

    # Default: bias search to Australia using country code
    return f"{q}, AU"


def score_location(loc, user_query):
    score = 0

    name = (loc.get("name") or "").lower()
    state = (loc.get("state") or "").lower()
    country = (loc.get("country") or "").lower()
    query = (user_query or "").lower().strip()

    query_parts = [part.strip() for part in query.split(",") if part.strip()]
    primary_name = query_parts[0] if query_parts else query


    if country == "au":
        score += 100

    if state in ["victoria", "vic"]:
        score += 50

    if name == primary_name:
        score += 40
    elif name.startswith(primary_name):
        score += 25
    elif primary_name in name:
        score += 15

    if "melbourne" in query:
        if state in ["victoria", "vic"]:
            score += 20

    return score


def geocode_location(query):
    api_key = st.secrets["api_keys"]["openweather"]
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    search_query = normalize_query(query)

    params = {
        "q": search_query,
        "limit": 8,
        "appid": api_key
    }

    try:
        response = requests.get(geo_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        ranked_places = sorted(
            data,
            key=lambda loc: score_location(loc, query),
            reverse=True
        )

        place = ranked_places[0]

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

    except Exception:
        return None


def get_weather_data(location_query=None):
    lat = -37.8136
    lon = 144.9631
    used_default_location = True
    location_error = None
    display_location = "Melbourne, VIC"

    # 1. Search overrides auto-location
    if isinstance(location_query, str) and location_query.strip():
            place = geocode_location(location_query)
            if place:
                lat, lon = place["lat"], place["lon"]
                used_default_location = False
                display_location = f"{place['name']}, {place.get('state', '')}"
            else:
                location_error = "Location not found"

        # CASE 2: location_query is a DICTIONARY (From your get_browser_location function)
    elif isinstance(location_query, dict) and location_query.get("success"):
            lat = location_query.get("latitude", lat)
            lon = location_query.get("longitude", lon)
            used_default_location = False
            # We use the reverse geocoder to turn lat/lon into a readable name like "Clayton, VIC"
            display_location = reverse_geocode_location(lat, lon)

        # CASE 3: No query provided, try to auto-fetch from session state
    elif location_query is None:
            browser_geo = get_browser_location()
            if browser_geo and isinstance(browser_geo, dict) and browser_geo.get("success"):
                lat = browser_geo.get("latitude", lat)
                lon = browser_geo.get("longitude", lon)
                used_default_location = False
                display_location = reverse_geocode_location(lat, lon)

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