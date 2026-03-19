import streamlit as st
from views.get_live_uv import get_weather_data, get_uv_protection_window
from datetime import datetime

def get_uv_style(uv):
    if uv <= 2:
        return "#22c55e", "Low"
    elif uv <= 5:
        return "#eab308", "Moderate"
    elif uv <= 7:
        return "#f97316", "High"
    elif uv <= 10:
        return "#ef4444", "Very High"
    else:
        return "#a855f7", "Extreme"
    
def get_uv_warning(uv):
    if uv <= 2:
        return "Low UV – minimal protection required. Enjoy your day outdoors."
    elif uv <= 5:
        return "Moderate UV – wear sunscreen and sunglasses when outdoors."
    elif uv <= 7:
        return "High UV – wear SPF30+ sunscreen, a hat and sunglasses."
    elif uv <= 10:
        return "Very High UV – reduce sun exposure between 10 AM and 4 PM."
    else:
        return "Extreme UV – avoid outdoor activities during peak hours."

def render(weather_data):
    st.markdown("""
    <style>
    /* 1. Target the top-most container padding */
    .block-container {
        padding-top: 0rem !important;
        margin-top: -2rem !important; /* Pulls content up into the empty header space */
    }

    /* 2. Remove the margin from the 'Search location' text itself */
    [data-testid="stMarkdownContainer"] h2, 
    [data-testid="stMarkdownContainer"] h3 {
        margin-top: 0rem !important;
        padding-top: 0.5rem !important;
    }

    /* 3. Completely collapse the header area */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* 4. Optional: Reduce gap between elements globally if needed */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    # Top spacing
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    if "active_location_query" not in st.session_state:
        st.session_state.active_location_query = None

    st.markdown("### Search location")
    col_input, col_btn, col_current = st.columns([6, 1.2, 1.8])

    with col_input:
        # We show what is currently in the session state
        location_query = st.text_input(
            "Search location",
            value=st.session_state.get("active_location_query", "") or "",
            placeholder="Enter suburb or city, e.g. Clayton, VIC",
            label_visibility="collapsed"
        )

    with col_btn:
        if st.button("Search", use_container_width=True):
            if location_query.strip():
                st.session_state.active_location_query = location_query.strip()
                st.rerun() # This triggers streamlit_app.py to fetch new weather

    with col_current:

        if st.button("Current", use_container_width=True):
            st.session_state.active_location_query = None
            # This clears the search so streamlit_app.py uses GPS
            st.rerun()

    if weather_data:
        uv_index = weather_data.get('current', {}).get('uvi', 0)
        start_time, end_time = get_uv_protection_window(weather_data)
        location_name = weather_data.get("display_location", "Location unavailable")
        used_default_location = weather_data.get("used_default_location", True)
        location_error = weather_data.get("location_error")
    else:
        uv_index = 0
        start_time, end_time = None, None
        location_name = "Location unavailable"
        used_default_location = True
        location_error = None
    
    if location_error == "Location not found":
        st.warning("Location not found. Showing default location.")
    elif location_error and used_default_location:
        st.info("Unable to detect your current location.")

    uv_index = round(uv_index) if uv_index is not None else 0

    peak_uv_text = f"{start_time} – {end_time}" if start_time and end_time else "No protection needed"

    if used_default_location and not st.session_state.active_location_query:
        location_name = f"{location_name}"
    # Location
    st.markdown(f"""
    <div style='text-align: center; margin: 0.8rem 0 1.6rem 0;'>
        <div style='
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.72rem 1.15rem;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(148,163,184,0.16);
            border-radius: 999px;
            box-shadow: 0 8px 24px rgba(15,23,42,0.06);
        '>
            <span style='font-size: 1rem;'>📍</span>
            <span style='
                color: #475569;
                font-size: 1.02rem;
                font-weight: 600;
                letter-spacing: -0.01em;
            '>
                {location_name}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # UV gauge centered
    uv_color, uv_level = get_uv_style(uv_index)
    uv_warning = get_uv_warning(uv_index)

    # UV gauge centered
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 1.5rem;'>
            <div style='border: 8px solid {uv_color}; width: 180px; height: 180px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <div style='font-size: 2rem; line-height: 1;'>☀️</div>
                <p style='font-size: 3.5rem; font-weight: bold; color: {uv_color}; margin: 0; line-height: 1;'>{uv_index}</p>
                <p style='font-size: 0.8rem; color: #6b7280; margin: 0; text-transform: uppercase;'>UV Index</p>
                <p style='font-size: 1.1rem; font-weight: bold; color: {uv_color}; margin: 0;'>{uv_level}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Warning banner
    st.markdown(f"""
    <div class='warning-banner' style='background: {uv_color};'>
        ⚠️ {uv_warning}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    # Section title
    st.markdown("""
    <h1 style='text-align: center; color: #1f2937; font-size: 2.5rem; margin-bottom: 2rem;'>
        Protection Advice
    </h1>
    """, unsafe_allow_html=True)

    # First row
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                💧
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Apply Sunscreen</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>SPF 30+ every 2 hours</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #c084fc 0%, #9333ea 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                🕶️
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Wear Sunglasses</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>UV protective lenses</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Second row
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                👒
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Wear a Hat</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>Wide-brimmed hat preferred</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='protection-card'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #34d399 0%, #059669 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;'>
                🌳
            </div>
            <h3 style='margin-bottom: 0.5rem; color: #1f2937; font-size: 1.8rem;'>Seek Shade</h3>
            <p style='color: #6b7280; font-size: 1rem; margin: 0;'>Stay indoors during peak UV hours</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 2.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    # Extra info cards
    info1, info2 = st.columns(2, gap="large")

    with info1:
        st.markdown(f"""
        <div class='card'>
            <h3 style='margin-top: 0; color: #1f2937;'>Today's UV Summary</h3>
            <p style='color: #6b7280; margin-bottom: 0.5rem;'>
                {uv_warning}
            </p>
            <ul style='color: #6b7280; padding-left: 1.2rem; margin-bottom: 0;'>
                <li>Peak UV hours: {peak_uv_text}</li>
                <li>Recommended SPF: 30+</li>
                <li>Reapply sunscreen every 2 hours</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with info2:
        st.markdown("""
        <div class='card'>
            <h3 style='margin-top: 0; color: #1f2937;'>Quick Tips</h3>
            <p style='color: #6b7280; margin-bottom: 0.5rem;'>
                Simple actions can reduce UV exposure significantly.
            </p>
            <ul style='color: #6b7280; padding-left: 1.2rem; margin-bottom: 0;'>
                <li>Check UV before leaving home</li>
                <li>Carry sunscreen in your bag</li>
                <li>Choose shaded outdoor areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin: 2.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)

    # CTA section
    cta_left, cta_center, cta_right = st.columns([0.12, 0.76, 0.12])

    with cta_center:
        st.markdown("""
        <div class='card' style='text-align: center; border: 1px solid #fdba74; background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);'>
            <div style='width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 1.6rem; color: white;
                        box-shadow: 0 6px 16px rgba(249,115,22,0.22);'>
                🧴
            </div>
            <div style='color:#9a3412; font-size:0.9rem; font-weight:700; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.35rem;'>
                Personalised Advice
            </div>
            <div style='color:#1f2937; font-size:2rem; font-weight:800; margin:0 0 0.6rem 0;'>
                Not sure about your skin type?
            </div>
            <div style='color:#6b7280; font-size:1rem; line-height:1.7; max-width:560px; margin:0 auto;'>
                Try our Skin Type Tool to discover your skin type and get sun protection advice tailored to you.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        btn_left, btn_center, btn_right = st.columns([0.22, 0.56, 0.22])
        with btn_center:
            if st.button("Try Skin Type Tool", use_container_width=True, key="skin_type_cta"):
                st.query_params["page"] = "skin-type-tool"
                st.rerun()