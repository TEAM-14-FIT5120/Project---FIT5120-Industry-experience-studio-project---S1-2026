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

    # Question 4
    st.markdown("#### 4. Do you have freckles on unexposed skin?")
    freckles = st.radio(
        "freckles",
        ["Many", "Several", "Few", "Very few", "None"],
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Submit button
    if st.button("🔍 Get My Skin Type & Protection Plan", use_container_width=True):
        # Simple logic to determine skin type
        score = 0
        
        # Calculate score based on answers
        if skin_color == "Very fair or pale":
            score += 0
        elif skin_color == "Fair":
            score += 1
        elif skin_color == "Medium":
            score += 2
        elif skin_color == "Olive or light brown":
            score += 3
        else:
            score += 4
            
        if sun_reaction == "Always burns, never tans":
            score += 0
        elif sun_reaction == "Burns easily, tans minimally":
            score += 1
        elif sun_reaction == "Burns moderately, tans gradually":
            score += 2
        elif sun_reaction == "Burns minimally, tans easily":
            score += 3
        else:
            score += 4