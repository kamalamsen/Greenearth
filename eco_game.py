import streamlit as st
import pandas as pd
from transformers import pipeline
from huggingface_hub import hf_hub_download
import base64

# --- Constants ---
MAX_SCORE = 12  # Update based on your scoring system
HF_REPO = "senkamalam/reward"
AUDIO_FILES = ["success.mp3", "level_up.mp3"]

# --- Error-Proof Audio System ---
def play_reward(sound_type: str):
    """Safely play audio rewards with fallbacks"""
    try:
        audio_file = hf_hub_download(
            repo_id=HF_REPO,
            filename=f"{sound_type}.mp3",
            repo_type="space",
            revision="main"
        )
        audio_html = f"""
        <audio controls autoplay style="display:none">
            <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_file, "rb").read()).decode()}">
        </audio>
        """
        st.components.v1.html(audio_html)
    except Exception as e:
        st.button("🎧 Play Sound", 
                help=f"Click to hear reward | Error: {str(e)}")

# --- Safe Score Calculation ---
def calculate_score(transport, diet, energy):
    """Validate and calculate score with error handling"""
    try:
        transport_scores = {
            "Car (Alone)": 4, 
            "Car (Carpool)": 3,
            "Public Transport": 2,
            "Bike/Walk": 1
        }
        diet_scores = {
            "Daily": 4,
            "3-4 times/week": 3,
            "1-2 times/week": 2,
            "Vegetarian/Vegan": 1
        }
        energy_scores = {
            "Non-Renewable (Grid)": 3,
            "Mixed Renewable": 2,
            "Solar/Wind": 1
        }
        
        return (
            transport_scores[transport] +
            diet_scores[diet] +
            energy_scores[energy]
        )
    except KeyError as e:
        st.error(f"Missing score value for: {str(e)}")
        return 0
    except Exception as e:
        st.error(f"Score calculation failed: {str(e)}")
        return 0

# --- Main App ---
def main():
    st.title("🌍 EcoGuardian Pro")
    st.markdown("### Track & Improve Your Environmental Impact")
    
    # --- Questionnaire ---
    with st.form("habits_form"):
        transport = st.selectbox(
            "🚗 Main Transportation:",
            ["Car (Alone)", "Car (Carpool)", "Public Transport", "Bike/Walk"]
        )
        
        diet = st.selectbox(
            "🍖 Meat Consumption:",
            ["Daily", "3-4 times/week", "1-2 times/week", "Vegetarian/Vegan"]
        )
        
        energy = st.selectbox(
            "💡 Energy Source:",
            ["Non-Renewable (Grid)", "Mixed Renewable", "Solar/Wind"]
        )
        
        if st.form_submit_button("Calculate My Impact"):
            try:
                # --- Calculate & Validate Score ---
                score = calculate_score(transport, diet, energy)
                progress_value = max(0.0, min(float(score)/MAX_SCORE, 1.0))
                
                # --- Display Results ---
                st.header("📊 Your Impact Report")
                cols = st.columns(3)
                cols[0].metric("Transport", transport_scores[transport])
                cols[1].metric("Diet", diet_scores[diet])
                cols[2].metric("Energy", energy_scores[energy])
                
                st.progress(progress_value)
                st.subheader(f"🌱 Sustainability Score: {score}/{MAX_SCORE}")
                
                # --- Rewards & Feedback ---
                if score >= 9:
                    play_reward("level_up")
                    st.balloons()
                    st.success("🌟 Earth Champion Level!")
                else:
                    play_reward("success")
                    st.info("💡 Let's improve together!")
                
                # --- AI Recommendations ---
                try:
                    generator = pipeline("text-generation", model="gpt2")
                    prompt = f"Give 3 simple sustainability tips for someone using {transport}, eating {diet}, with {energy} energy:"
                    tips = generator(prompt, max_length=200)[0]['generated_text']
                    st.markdown(f"**Recommended Actions:**\n\n{tips.split(':')[-1]}")
                except Exception as e:
                    st.warning(f"AI suggestions unavailable: {str(e)}")
                    
            except Exception as e:
                st.error(f"App error: {str(e)}")

# --- Run App ---
if __name__ == "__main__":
    main()
