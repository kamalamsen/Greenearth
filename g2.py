import streamlit as st
import pandas as pd
from transformers import pipeline

# Title and Introduction
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
    st.info("**Why this matters:** Transportation accounts for 29% of greenhouse gas emissions. Switching to sustainable options can reduce your carbon footprint by up to 50%!")

# Category 2: Diet
with st.expander("🍔 Dietary Choices"):
    diet = st.selectbox("How often do you consume animal products?", 
                       ["Daily", "3-4 times/week", "1-2 times/week", "Vegetarian/Vegan"])
    st.info("**Did you know?** A plant-based diet reduces food-related emissions by 73% (Oxford Study).")

# Category 3: Energy
with st.expander("💡 Home Energy Use"):
    energy = st.selectbox("Your primary energy source:", 
                         ["Non-Renewable (Grid)", "Solar/Wind", "Mixed Renewable"])
    st.info("**Good to know:** Renewable energy can reduce home emissions by 80% compared to fossil fuels.")

# --- Score Calculation ---
score = 0

# Transportation Scoring
transport_scores = {
    "Car (Alone)": 4, 
    "Car (Carpool)": 3,
    "Public Transport": 2,
    "Bike/Walk": 1
}

# Diet Scoring
diet_scores = {
    "Daily": 4,
    "3-4 times/week": 3,
    "1-2 times/week": 2,
    "Vegetarian/Vegan": 1
}

# Energy Scoring
energy_scores = {
    "Non-Renewable (Grid)": 3,
    "Mixed Renewable": 2,
    "Solar/Wind": 1
}

score = transport_scores[transport] + diet_scores[diet] + energy_scores[energy]

# --- Results Dashboard ---
st.header("📊 Your Environmental Impact")

# Visual Score Display
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Transport Score", transport_scores[transport], help="Lower is better")
with col2:
    st.metric("Diet Score", diet_scores[diet], help="Lower is better")
with col3:
    st.metric("Energy Score", energy_scores[energy], help="Lower is better")

# Total Score with Visual Feedback
st.subheader(f"Your Total GreenScore: {score}/9")
if score <= 3:
    st.success("🌍 Eco Champion! You're making exceptional sustainable choices!")
elif score <= 6:
    st.warning("🌱 Green Starter! Great foundation with room for improvement!")
else:
    st.error("⚠️ Improvement Needed! Let's work on reducing your footprint!")

# --- Personalized Feedback Section ---
st.header("💡 Personalized Action Plan")

# AI Feedback with Error Handling
try:
    # Load AI Model (Lighter Model for Better Performance)
    feedback_model = pipeline("text-generation", model="distilgpt2")
    if feedback_model:
        feedback_prompt = f"Suggest simple eco-friendly actions for someone with these habits: Transportation={transport}, Diet={diet}, Energy={energy}. Keep it short and practical."
        ai_feedback = feedback_model(feedback_prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        st.markdown(f"**AI-Powered Recommendations:** {ai_feedback}")
    else:
        st.warning("AI model couldn't load. Try restarting the app.")
except Exception as e:
    st.warning("AI recommendations are temporarily unavailable.")
    st.error(f"Error: {e}")

# --- Achievement System ---
st.header("🏆 Earn Eco-Badges")

badges = {
    "Green Novice": score <= 6,
    "Public Commuter": transport in ["Public Transport", "Bike/Walk"],
    "Plant Pioneer": diet in ["1-2 times/week", "Vegetarian/Vegan"],
    "Energy Saver": energy != "Non-Renewable (Grid)"
}

cols = st.columns(4)
for idx, (badge, earned) in enumerate(badges.items()):
    with cols[idx % 4]:
        st.image("https://img.icons8.com/color/48/medal.png" if earned else "https://img.icons8.com/color/48/medal--v1.png", 
                width=40)
        st.caption(f"{'✅ ' if earned else '🔒 '}{badge}")

# --- Progress Tracking ---
st.header("📈 Progress Tracker")
if 'history' not in st.session_state:
    st.session_state.history = []

if st.button("Save Current Score"):
    st.session_state.history.append({
        "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "score": score
    })
    
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.line_chart(history_df.set_index('date'))
else:
    st.info("Save your first score to start tracking progress!")

# --- Educational Resources ---
st.header("📚 Learn More")
with st.expander("Why This Matters"):
    st.markdown("""
    - 🌡️ The average American carbon footprint is 16 tons/year
    - 🌳 It takes 7 trees to offset 1 ton of CO2
    - 🚲 Biking instead of driving just 10 miles/week saves 500 lbs CO2/year
    """)

with st.expander("Actionable Tips"):
    st.markdown("""
    - **Transport:** Try carpooling 2 days/week (saves 1,600 lbs CO2/year)
    - **Diet:** Meat-free Mondays (saves 1,900 lbs CO2/year)
    - **Energy:** Switch to LED bulbs (saves 1,000 lbs CO2/year)
    """)

# --- Footer ---
st.markdown("---")


st.markdown("🌍 *Small actions lead to a greener planet!*")
