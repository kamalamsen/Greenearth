import streamlit as st
import pandas as pd
from transformers import pipeline
from huggingface_hub import hf_hub_download
import base64

# --- Constants ---
MAX_SCORE = 9  # 3 categories × max 3 points each
HF_REPO = "senkamalam/reward"

# --- Scoring System Explanation ---
SCORING_LOGIC = """
### 🧮 How Scoring Works:
- **Transportation**:  
  🚗 Car (1pt) → 🚌 Bus/Train (2pts) → 🚲 Bike/Walk (3pts)  
- **Diet**:  
  🥩 Daily Meat (1pt) → 🐟 Weekly (2pts) → 🌱 Vegetarian (3pts)  
- **Energy**:  
  🔌 Regular Power (1pt) → 🌤️ Some Green (2pts) → 💨 All Renewable (3pts)  

**Maximum Possible Score: 9** (3pts × 3 categories)
"""

# --- Initialize Session State ---
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- Audio Reward System ---
def play_sound(sound_type: str):
    """Play audio feedback"""
    # ... (keep existing audio code) ...

# --- Score Calculation ---
def calculate_score(transport, diet, energy):
    """Clearer scoring system with better points distribution"""
    score_map = {
        # Transportation (more eco-friendly = higher points)
        "Car": 1, "Bus/Train": 2, "Bike/Walk": 3,
        # Diet (less meat = higher points)
        "Daily": 1, "Weekly": 2, "Sometimes": 3, "Never": 3,
        # Energy (greener = higher points)
        "Regular Power": 1, "Some Green Energy": 2, "All Renewable": 3
    }
    return score_map[transport] + score_map[diet] + score_map[energy]

# --- Main App ---
def main():
    st.title("🌍 EcoGame Pro")
    st.markdown("### Track & Improve Your Environmental Impact")
    
    # Show scoring explanation first
    with st.expander("📊 HOW SCORING WORKS", expanded=True):
        st.markdown(SCORING_LOGIC)
    
    # --- User Inputs ---
    with st.expander("📝 YOUR HABITS", expanded=True):
        transport = st.selectbox(
            "Main Transportation:",
            ["Car", "Bus/Train", "Bike/Walk"],
            index=0,
            help="More eco-friendly choices give higher points!"
        )
        
        diet = st.select_slider(
            "Meat Consumption:",
            options=["Daily", "Weekly", "Sometimes", "Never"],
            value="Daily",
            help="Less meat consumption = higher score"
        )
        
        energy = st.radio(
            "Energy Source:",
            ["Regular Power", "Some Green Energy", "All Renewable"],
            index=0,
            help="Greener energy sources boost your score"
        )
    
    # --- Calculate & Display Score ---
    current_score = calculate_score(transport, diet, energy)
    progress_value = current_score/MAX_SCORE
    
    st.subheader("📊 Your Results")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Transport", f"{calculate_score(transport, '', '')}/3")
    with cols[1]:
        st.metric("Diet", f"{calculate_score('', diet, '')}/3")
    with cols[2]:
        st.metric("Energy", f"{calculate_score('', '', energy)}/3")
    
    st.progress(progress_value)
    st.subheader(f"🏆 Total Eco Score: {current_score}/{MAX_SCORE}")
    
    # --- Visual Feedback ---
    if current_score >= 7:
        st.success("🌟 Eco Champion! Keep up the great work!")
        play_sound("success")
    elif current_score >= 4:
        st.warning("🔄 Good start! Try our challenges below to improve")
    else:
        st.error("🌱 Room for growth - check our eco tips!")

# ... (keep rest of the code same) ...

if __name__ == "__main__":
    main()
