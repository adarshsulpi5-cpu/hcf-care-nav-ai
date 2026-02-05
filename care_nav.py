import streamlit as st
from groq import Groq  # Or from transformers import pipeline
import speech_recognition as sr
from gtts import gTTS
import os

client = Groq(api_key="your_groq_key")  # Free at groq.com

# Pre-defined destinations & simple paths (use dict for real maps)
destinations = {
    "cardiology": "Floor 2, Room 205 - Take elevator, turn left",
    "emergency": "Ground Floor ER - Fastest route: Straight ahead!",
    "radiology": "Basement - Take stairs down"
}

st.title("🩺 CareNav AI – Your Hospital Guide")

# Voice Input
if st.button("Speak Your Query"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        query = r.recognize_google(audio)
        st.write("You said:", query)
else:
    query = st.text_input("Or type: e.g., 'chest pain' or 'where is cardiology?'")

if query:
    # LLM Prompt for intent
    prompt = f"""Extract destination from query: '{query}'. 
    If emergency symptoms (pain, bleeding, dizzy), prioritize 'emergency'.
    Output only key: cardiology, emergency, radiology, etc."""
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    dest = response.choices[0].message.content.strip().lower()
    
    if dest in destinations:
        path = destinations[dest]
        st.success(f"Go to: {dest.upper()}")
        st.info(f"Directions: {path}")
        if "emergency" in dest:
            st.warning("🚨 Emergency detected! Follow fastest route & stay calm.")
        
        # Show map (upload your floor plan images)
        st.image("hospital_floor1.jpg", caption="Your Path Highlighted")
        
        # Voice output
        tts = gTTS(path)
        tts.save("directions.mp3")
        st.audio("directions.mp3")
    else:
        st.error("Sorry, try again or ask front desk!")
