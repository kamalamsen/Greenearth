import streamlit as st
import pandas as pd
from transformers import pipeline
from huggingface_hub import hf_hub_download
import base64

# --- Audio Reward System ---
def play_reward(sound_type: str):
    """Play audio rewards from your HF Space"""
    try:
        # Get audio from your Hugging Face Space
        audio_file = hf_hub_download(
            repo_id="senkamalam/reward",
            filename=f"{sound_type}.mp3",
            repo_type="space"
        )
        
        # Create audio player with visible controls
        audio_html = f"""
        <audio controls {'autoplay' if sound_type == 'success' else ''}>
            <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_file, "rb").read()).decode()}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.button("🔊 Play Reward Sound", 
                help=f"Click to hear your achievement! Error: {str(e)}")

# --- Visual Celebration ---        
def show_celebration():
    st.markdown("""
    <style>
    .celebrate {
        animation: bounce 1s infinite;
        font-size: 48px;
        text-align: center;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    </style>
    <div class="celebrate">🎉 🌍 🎉</div>
    """, unsafe_allow_html=True)
    st.balloons()

# --- Main App ---
st.title("🌱 EcoGuardian Pro")
st.markdown("### Your Personal Sustainability Tracker")

# --- Questionnaire ---
transport = st.selectbox(
    "🚗 Main Transportation:",
    ["Car", "Bus/Train", "Bike/Walk"],
    help="Transportation contributes 29% of global emissions"
)

diet = st.select_slider(
    "🍖 Meat Consumption:",
    options=["Daily", "Weekly", "Occasionally", "Never"],
    value="Daily"
)

energy = st.radio(
    "💡 Energy Source:",
    ["Fossil Fuels", "Mixed", "Renewable"]
)

# --- Score Calculation ---
SCORES = {
    "Car": 4, "Bus/Train": 2, "Bike/Walk": 1,
    "Daily": 4, "Weekly": 3, "Occasionally": 2, "Never": 1,
    "Fossil Fuels": 3, "Mixed": 2, "Renewable": 1
}

score = sum([SCORES[transport], SCORES[diet], SCORES[energy]])

# --- Results Display ---
st.header("📊 Your Impact Report")
col1, col2, col3 = st.columns(3)
col1.metric("Transport", SCORES[transport], delta_color="inverse")
col2.metric("Diet", SCORES[diet], delta_color="inverse")
col3.metric("Energy", SCORES[energy], delta_color="inverse")

st.progress(score/9)
st.subheader(f"🌍 Sustainability Score: {score}/9")

# --- Rewards System ---
if st.button("💡 Get Personalized Plan"):
    show_celebration()
    play_reward("success")
    
    try:
        # AI Recommendations
        generator = pipeline("text-generation", model="gpt2")
        prompt = f"Give 3 simple tips to improve sustainability for someone using {transport}, eating meat {diet}, and using {energy} energy:"
        tips = generator(prompt, max_length=200)[0]['generated_text']
        st.success(f"**Your Action Plan:**\n\n{tips.split(':')[-1]}")
        
    except Exception as e:
        st.warning(f"AI suggestions unavailable: {str(e)}")

