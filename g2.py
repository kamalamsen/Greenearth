import streamlit as st
import pandas as pd
import openai

# OpenAI API Key Handling (Ensure it's set properly)
if "openai_api_key" in st.secrets:
    openai.api_key = st.secrets["openai_api_key"]
else:
    st.error("OpenAI API key is missing. Please add it to Streamlit Secrets.")
    st.stop()

st.title("🌱 GreenScore AI")
st.markdown("""
**Empowering you to reduce your environmental footprint, one step at a time!**
Track your eco-impact, get personalized advice, and earn rewards for sustainable choices.
""")

# --- Questionnaire Section ---
st.header("📝 Lifestyle Assessment")

# Category 1: Transportation
with st.expander("🚗 Transportation Habits"):
    transport = st.selectbox("How do you commute regularly?", 
                            ["Car (Alone)", "Car (Carpool)", "Public Transport", "Bike/Walk"])

# Category 2: Diet
with st.expander("🍔 Dietary Choices"):
    diet = st.selectbox("How often do you consume animal products?", 
                       ["Daily", "3-4 times/week", "1-2 times/week", "Vegetarian/Vegan"])

# Category 3: Energy
with st.expander("💡 Home Energy Use"):
    energy = st.selectbox("Your primary energy source:", 
                         ["Non-Renewable (Grid)", "Solar/Wind", "Mixed Renewable"])

# --- GPT-Powered Personalized Feedback Section ---
st.header("💡 Personalized Action Plan")

def get_gpt_tips(transport, diet, energy):
    prompt = f"""
    Generate 3-5 eco-friendly tips in bullet points for a person with these habits:
    - Transportation: {transport}
    - Diet: {diet}
    - Energy: {energy}
    The tips should be short, practical, and highly actionable.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract bullet points from response
        gpt_output = response["choices"][0]["message"]["content"]
        return gpt_output.split("\n")  # Ensures list format
    except Exception as e:
        st.error(f"Error fetching GPT response: {e}")
        return []

# Call GPT function based on user inputs
tips = get_gpt_tips(transport, diet, energy)

# Display in Streamlit
st.markdown("### 🔹 AI-Powered Eco-Friendly Tips Just for You:")
for tip in tips:
    if tip.strip():  # Avoid blank lines
        st.markdown(f"- {tip}")
