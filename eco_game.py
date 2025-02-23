import streamlit as st
import pandas as pd
from transformers import pipeline
import base64
import platform
import asyncio

# --- Core Improvements ---
# 1. Simple Language | 2. Voice Rewards | 3. Score Boosts | 4. Clear Captions

# --- Audio Reward System ---
from huggingface_hub import hf_hub_download
import base64

def play_sound(sound_type: str):
    """Play audio from Hugging Face repo"""
    try:
        audio_file = hf_hub_download(
            repo_id="senkamalam/reward", 
            filename=f"{sound_type}.mp3",
            repo_type="space"
        )
        with open(audio_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            html = f"""
            <audio controls autoplay style="display:none">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Sound system unavailable: {str(e)}")
    try:
        with open(sounds[sound_type], "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(html, unsafe_allow_html=True)
            st.caption(f"🎉 Achievement unlocked!")  # Visual caption
    except:
        st.warning("Couldn't play reward sound")

# --- Simplified AI Feedback ---
@st.cache_resource
def get_eco_tips(_transport, _diet, _energy):
    """Generate easy-to-understand tips with score boost info"""
    try:
        generator = pipeline("text-generation", model="gpt2")
        prompt = f"""Create 3 simple eco-tips for someone who:
        - Travels by {_transport}
        - Eats meat {_diet}
        - Uses {_energy} energy
        
        Format each tip:
        🌿 [Action] (+[Points] points)
        💡 Example: "Take bus instead of car (+2 points)"
        """
        
        response = generator(prompt, max_length=250)[0]['generated_text']
        return response.split("Example:")[-1].strip().replace("- ", "\n\n")
    except:
        return None

# --- Score Boost System ---
ECO_CHALLENGES = [
    {"icon": "🚌", "task": "Use public transport", "points": 2},
    {"icon": "🥗", "task": "Vegetarian meal day", "points": 3},
    {"icon": "💡", "task": "1hr less electricity", "points": 1}
]

# --- Main App Interface ---
st.title("🌱 EcoFriend")
st.markdown("### Simple steps to help our planet!")

# --- User Input Section ---
with st.expander("📝 Tell me about your habits", expanded=True):
    transport = st.selectbox(
        "How do you usually travel?",
        ["Car", "Bus/Train", "Bike/Walk"],
        help="Transportation makes ~30% of carbon emissions"
    )
    
    diet = st.select_slider(
        "How often do you eat meat?",
        options=["Daily", "Weekly", "Sometimes", "Never"],
        value="Daily"
    )
    
    energy = st.radio(
        "Home energy type:",
        ["Regular Power", "Some Green Energy", "All Renewable"],
        index=0
    )

# --- Calculate Base Score ---
score = 0  # Add your scoring logic here

# --- AI Tips Section ---
st.header("💡 Your Personal Eco Plan")
if st.button("Get Custom Tips", help="Get easy ways to improve"):
    tips = get_eco_tips(transport, diet, energy)
    if tips:
        st.success("Here's your simple action plan:")
        st.markdown(tips)
        play_sound("success")
        st.caption("Complete these to boost your score!") 
    else:
        st.info("Tips coming soon! Try the challenges below")

# --- Daily Challenges ---
st.header("🎯 Daily Quick Wins")
cols = st.columns(3)
for idx, challenge in enumerate(ECO_CHALLENGES):
    with cols[idx]:
        if st.button(f"{challenge['icon']} {challenge['task']}"):
            score += challenge['points']
            st.session_state.score = score
            st.balloons()
            play_sound("cheer")
            st.toast(f"+{challenge['points']} points! Great job!")

# --- Progress Tracking ---
st.header("📈 Your Progress")
if 'score' not in st.session_state:
    st.session_state.score = 0

st.subheader(f"Current Score: {st.session_state.score}")
st.progress(st.session_state.score/30)  # Adjust max score

# --- Level System ---
if st.session_state.score >= 20:
    st.success("🌟 Earth Hero Level!")
    play_sound("levelup")
elif st.session_state.score >= 10:
    st.warning("🌿 Green Learner Level")

# --- How It Works ---
with st.expander("❓ Understanding Your Score"):
    st.markdown("""
    - **Goal**: Lower score = Better for Earth 🌍
    - **Improve by**:
      - Using green transport (+2 points)
      - Eating plant-based meals (+3 points)
      - Conserving energy (+1 point)
    - Earn badges at 10/20/50 points!
    """)

# --- Run App ---
if __name__ == "__main__":
    import sys
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if '--server.fileWatcherType' not in sys.argv:
        sys.argv += ['--server.fileWatcherType', 'none']
