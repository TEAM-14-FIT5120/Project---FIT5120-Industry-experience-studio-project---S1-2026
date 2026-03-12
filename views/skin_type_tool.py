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

        # Determine skin type
        if score <= 2:
            skin_type = "Type I"
            skin_type_name = "Very Fair"
            risk_level = "Extreme Risk"
            risk_color = "#dc2626"
            recommendations = [
                "🧴 Apply SPF 50+ sunscreen every 90 minutes",
                "👒 Always wear a wide-brimmed hat outdoors",
                "👕 Wear long sleeves and pants when possible",
                "😎 UV-blocking sunglasses are essential",
                "🌳 Seek shade between 10am-4pm",
                "⏰ Limit sun exposure to less than 30 minutes",
                "🚫 Avoid tanning beds completely"
            ]
        elif score <= 5:
            skin_type = "Type II"
            skin_type_name = "Fair"
            risk_level = "High Risk"
            risk_color = "#ea580c"
            recommendations = [
                "🧴 Apply SPF 30-50 sunscreen every 2 hours",
                "👒 Wear a hat when outdoors for extended periods",
                "👕 Cover up during peak sun hours",
                "😎 Wear UV-protective sunglasses",
                "🌳 Seek shade during midday hours",
                "⏰ Build up sun exposure gradually",
                "📱 Use UV index apps to plan activities"
            ]
        elif score <= 9:
            skin_type = "Type III"
            skin_type_name = "Medium"
            risk_level = "Moderate Risk"
            risk_color = "#f59e0b"
            recommendations = [
                "🧴 Apply SPF 30+ sunscreen every 2-3 hours",
                "👒 Wear a hat during extended outdoor activities",
                "😎 Use UV-protective sunglasses",
                "🌳 Take shade breaks during peak hours",
                "⏰ Reapply sunscreen after swimming",
                "🏖️ Be extra cautious at beach or pool",
                "📊 Monitor UV index daily"
            ]
        elif score <= 13:
            skin_type = "Type IV"
            skin_type_name = "Olive"
            risk_level = "Moderate Risk"
            risk_color = "#f59e0b"
            recommendations = [
                "🧴 Apply SPF 30 sunscreen every 3 hours",
                "😎 Wear sunglasses for eye protection",
                "👒 Hat recommended for extended exposure",
                "🌳 Seek shade when UV index is high",
                "⏰ Reapply after swimming or sweating",
                "🏖️ Extra protection at beach/snow",
                "✅ Still vulnerable to UV damage"
            ]
        else:
            skin_type = "Type V-VI"
            skin_type_name = "Dark"
            risk_level = "Lower Risk"
            risk_color = "#10b981"
            recommendations = [
                "🧴 Apply SPF 15-30 sunscreen daily",
                "😎 Wear sunglasses for eye protection",
                "⏰ Reapply sunscreen every 3-4 hours",
                "🏖️ Extra protection during water activities",
                "🌳 Shade recommended during peak UV",
                "✅ Still need sun protection",
                "📊 Check UV index for outdoor planning"
            ]
        
        # Display results
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {risk_color}20 0%, {risk_color}10 100%); 
             padding: 2rem; border-radius: 12px; border-left: 4px solid {risk_color};'>
            <h2 style='margin: 0 0 1rem 0;'>Your Results</h2>
            <div style='display: flex; gap: 2rem; align-items: center; flex-wrap: wrap;'>
                <div>
                    <p style='margin: 0; color: #6b7280; font-size: 0.875rem;'>Fitzpatrick Skin Type</p>
                    <p style='margin: 0.25rem 0 0 0; font-size: 2rem; font-weight: 700; color: {risk_color};'>
                        {skin_type}
                    </p>
                    <p style='margin: 0.25rem 0 0 0; color: #6b7280;'>{skin_type_name} Skin</p>
                </div>
                <div>
                    <p style='margin: 0; color: #6b7280; font-size: 0.875rem;'>UV Risk Level</p>
                    <p style='margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 600; color: {risk_color};'>
                        {risk_level}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Personalized Protection Recommendations")
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        
        for rec in recommendations:
            st.markdown(f"""
            <div style='background: #f9fafb; padding: 0.75rem 1rem; border-radius: 8px; 
                 margin-bottom: 0.5rem; border-left: 3px solid {risk_color};'>
                {rec}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # Additional info
        st.info("💡 **Remember:** All skin types can develop skin cancer. Always practice sun safety!")
    
    # Educational content
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📚 Understanding Fitzpatrick Skin Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Type I-II (Fair Skin)**
        - Always or easily burns
        - Never or rarely tans
        - Highest risk of skin damage
        - Requires maximum protection
        """)
        
        st.markdown("""
        **Type III-IV (Medium to Olive)**
        - Sometimes burns
        - Tans gradually to moderately
        - Moderate risk of skin damage
        - Requires regular protection
        """)
    
    with col2:
        st.markdown("""
        **Type V-VI (Dark Skin)**
        - Rarely burns
        - Tans easily and deeply
        - Lower but still present risk
        - Still needs sun protection
        """)
        
        st.markdown("""
        **Important Note**
        - All skin types need UV protection
        - Skin cancer can affect anyone
        - Regular skin checks recommended
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)