import streamlit as st
import pandas as pd
from transformers import pipeline
from huggingface_hub import hf_hub_download
import base64

# --- Constants ---
MAX_SCORE = 30
HF_REPO = "senkamalam/reward"
INITIAL_SCORE = 0

# --- Initialize Session State ---
if 'score' not in st.session_state:
    st.session_state.score = INITIAL_SCORE

# --- Audio Reward System ---
def play_sound(sound_type: str):
    """Play audio from your Hugging Face Space"""
    try:
        # Download from your HF Space
        audio_file = hf_hub_download(
            repo_id=HF_REPO,
            filename=f"{sound_type}.mp3",
            repo_type="space"
        )
        
        # Create hidden audio player
        with open(audio_file, "rb") as f:
            audio_data = f.read()
            b64 = base64.b64encode(audio_data).decode()
            audio_html = f"""
            <audio controls autoplay style="display:none">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            
    except Exception as e:
        st.warning(f"🔇 Sound system: {str(e)}")

# --- Score Calculation ---
def calculate_score(transport, diet, energy):
    """Simple scoring system"""
    score_map = {
        "Car": 4, "Bus/Train": 2, "Bike/Walk": 1,
        "Daily": 4, "Weekly": 3, "Sometimes": 2, "Never": 1,
        "Regular Power": 3, "Some Green Energy": 2, "All Renewable": 1
    }
    return (
        score_map[transport] + 
        score_map[diet] + 
        score_map[energy]
    )

# --- Main App ---
def main():
    st.title("🌍 EcoGame Pro")
    st.markdown("### Track & Improve Your Environmental Impact")
    
    # --- User Inputs ---
    with st.expander("📝 Your Habits", expanded=True):
        transport = st.selectbox(
            "Main Transportation:",
            ["Car", "Bus/Train", "Bike/Walk"],
            index=0
        )
        
        diet = st.select_slider(
            "Meat Consumption:",
            options=["Daily", "Weekly", "Sometimes", "Never"],
            value="Daily"
        )
        
        energy = st.radio(
            "Energy Source:",
            ["Regular Power", "Some Green Energy", "All Renewable"],
            index=0
        )
    
    # --- Calculate Score ---
    current_score = calculate_score(transport, diet, energy)
    st.session_state.score += current_score
    
    # --- Progress System ---
    progress_value = min(st.session_state.score/MAX_SCORE, 1.0)
    st.progress(progress_value)
    st.subheader(f"🏆 Current Score: {st.session_state.score}/{MAX_SCORE}")
    
    # --- Rewards ---
    if st.button("🎮 Get Eco Tips"):
        try:
            # AI Recommendations
            generator = pipeline("text-generation", model="gpt2")
            prompt = f"Give 3 simple tips to improve sustainability for someone using {transport}, eating meat {diet}, using {energy} energy:"
            response = generator(prompt, max_length=200)[0]['generated_text']
            st.success(f"**Your Eco Plan:**\n\n{response.split(':')[-1]}")
            play_sound("success")
            
        except Exception as e:
            st.warning(f"AI system busy - try again later! {str(e)}")
    
    # --- Challenges ---
    st.header("🚀 Daily Challenges")
    challenges = [
        {"name": "🚌 Public Transport Day", "points": 2},
        {"name": "🥗 Veg Meal Day", "points": 3},
        {"name": "💡 Lights Off Hour", "points": 1}
    ]
    
    cols = st.columns(3)
    for idx, challenge in enumerate(challenges):
        with cols[idx]:
            if st.button(f"{challenge['name']} (+{challenge['points']})"):
                st.session_state.score += challenge['points']
                play_sound("level_up")
                st.balloons()
                st.toast(f"🎉 +{challenge['points']} Points!")

# --- Run App ---
if __name__ == "__main__":
    main()
