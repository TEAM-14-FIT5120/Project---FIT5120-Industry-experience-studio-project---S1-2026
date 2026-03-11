"""
Skin Type Tool - Personalized protection recommendations
"""
import streamlit as st

def render():
    st.title("Skin Type Protection Tool")
    st.markdown("""
    <p style='font-size: 1.125rem; color: #6b7280; margin-bottom: 3rem;'>
        Answer a few questions to get personalized sun protection recommendations based on your skin type.
    </p>
    """, unsafe_allow_html=True)
    
    # Quiz Section
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📋 Skin Type Assessment Quiz")
    
    # Question 1
    st.markdown("#### 1. What is your natural skin color (before sun exposure)?")
    skin_color = st.radio(
        "skin_color",
        ["Very fair or pale", "Fair", "Medium", "Olive or light brown", "Brown or dark brown"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Question 2
    st.markdown("#### 2. How does your skin typically react to the first sun exposure in summer?")
    sun_reaction = st.radio(
        "sun_reaction",
        ["Always burns, never tans", "Burns easily, tans minimally", 
         "Burns moderately, tans gradually", "Burns minimally, tans easily", 
         "Rarely burns, tans very easily"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Question 3
    st.markdown("#### 3. What is your natural hair color?")
    hair_color = st.radio(
        "hair_color",
        ["Red or light blonde", "Blonde", "Light brown", "Dark brown", "Black"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)