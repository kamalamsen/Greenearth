import streamlit as st
from huggingface_hub import hf_hub_download
import base64

# --- Constants ---
MAX_SCORE = 9  # 3 categories × max 3 points each
HF_REPO = "senkamalam/reward"

# --- Scoring System ---
SCORING_LOGIC = """
### 🧮 Scoring System
**Transportation**  
🚗 Car (1pt) → 🚌 Bus/Train (2pts) → 🚲 Bike/Walk (3pts)  

**Diet**  
🥩 Daily Meat (1pt) → 🐟 Weekly (2pts) → 🌱 Vegetarian (3pts)  

**Energy**  
🔌 Regular Power (1pt) → 🌤️ Some Green (2pts) → 💨 All Renewable (3pts)  

**Maximum Score:** 9 points (3pts × 3 categories)
"""

# --- Initialize Session State ---
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- Audio System ---
def play_sound(sound_type: str):
    """Play feedback sounds from Hugging Face Space"""
    try:
        audio_file = hf_hub_download(
            repo_id=HF_REPO,
            filename=f"{sound_type}.mp3",
            repo_type="space"
        )
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
        st.warning(f"🔇 Sound error: {str(e)}")

# --- Scoring Functions ---
def get_transport_score(transport: str) -> int:
    """Calculate transportation score"""
    scores = {"Car": 1, "Bus/Train": 2, "Bike/Walk": 3}
    return scores.get(transport, 0)

def get_diet_score(diet: str) -> int:
    """Calculate diet score"""
    scores = {"Daily": 1, "Weekly": 2, "Sometimes": 3, "Never": 3}
    return scores.get(diet, 0)

def get_energy_score(energy: str) -> int:
    """Calculate energy score"""
    scores = {"Regular Power": 1, "Some Green Energy": 2, "All Renewable": 3}
    return scores.get(energy, 0)

def calculate_total_score(transport: str, diet: str, energy: str) -> int:
    """Calculate total eco score"""
    return (
        get_transport_score(transport) +
        get_diet_score(diet) +
        get_energy_score(energy)
    )

# --- Main App ---
def main():
    st.title("🌍 EcoGame Pro")
    st.markdown("### Track & Improve Your Environmental Impact")
    
    # Scoring explanation
    with st.expander("📊 HOW SCORING WORKS", expanded=True):
        st.markdown(SCORING_LOGIC)
    
    # User inputs
    with st.expander("📝 YOUR HABITS", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transport = st.selectbox(
                "Transportation:",
                ["Car", "Bus/Train", "Bike/Walk"],
                index=0
            )
            
        with col2:
            diet = st.select_slider(
                "Meat Consumption:",
                options=["Daily", "Weekly", "Sometimes", "Never"],
                value="Daily"
            )
            
        with col3:
            energy = st.radio(
                "Energy Source:",
                ["Regular Power", "Some Green Energy", "All Renewable"],
                index=0
            )
    
    # Calculate scores
    try:
        transport_score = get_transport_score(transport)
        diet_score = get_diet_score(diet)
        energy_score = get_energy_score(energy)
        total_score = transport_score + diet_score + energy_score
        
        # Display results
        st.subheader("📊 Your Results")
        cols = st.columns(3)
        cols[0].metric("Transport", f"{transport_score}/3")
        cols[1].metric("Diet", f"{diet_score}/3")
        cols[2].metric("Energy", f"{energy_score}/3")
        
        # Progress and feedback
        progress = total_score / MAX_SCORE
        st.progress(progress)
        st.subheader(f"🏆 Total Score: {total_score}/{MAX_SCORE}")
        
        # Visual feedback
        if total_score >= 7:
            st.success("🌟 Eco Champion! Keep up the great work!")
            play_sound("success")
        elif total_score >= 4:
            st.warning("🔄 Good start! Try our challenges to improve")
        else:
            st.error("🌱 Room for growth - check our eco tips below!")
            
    except KeyError as e:
        st.error(f"⚠️ Error calculating scores: Invalid input detected")
        st.stop()

    # Eco Tips Section
    st.divider()
    if st.button("💡 Get Personalized Eco Tips"):
        try:
            generator = pipeline("text-generation", model="gpt2")
            prompt = f"Give 3 practical tips for someone using {transport}, eating meat {diet}, using {energy}:"
            response = generator(prompt, max_length=200)[0]['generated_text']
            st.success(f"**Your Eco Plan:**\n\n{response.split(':')[-1]}")
            play_sound("success")
        except Exception as e:
            st.warning(f"⚠️ AI system busy - try again later! Error: {str(e)}")

    # Daily Challenges
    st.divider()
    st.header("🚀 Daily Challenges")
    challenges = [
        {"name": "🚌 Public Transport Day", "points": 2},
        {"name": "🥗 Veg Meal Day", "points": 3},
        {"name": "💡 Lights Off Hour", "points": 1}
    ]
    
    cols = st.columns(3)
    for idx, challenge in enumerate(challenges):
        with cols[idx]:
            if st.button(f"{challenge['name']}\n(+{challenge['points']} pts)"):
                st.session_state.score += challenge['points']
                play_sound("level_up")
                st.balloons()
                st.toast(f"🎉 Earned {challenge['points']} points!")

if __name__ == "__main__":
    main()
