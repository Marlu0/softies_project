import streamlit as st
from src.speech2text import listen_for_input
from src.text2speech import speak_text
from src.context_creator import create_context

# Streamlit page setup
st.set_page_config(page_title="🎙️ Voice Assistant Chat", layout="centered")
st.title("🎙️ Voice Assistant Chat")

# Instructions for the user
st.write("Welcome to the speech recognition and text-to-speech app. Speak continuously to interact with the assistant.")

# Initialize conversation history in session_state if it doesn't exist
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Function to display the conversation (user input and assistant's reply)
def display_conversation():
    for message in st.session_state.conversation_history:
        if message['role'] == 'user':
            st.write(f"🎤 **You**: {message['text']}")
        else:
            st.write(f"🤖 **Assistant**: {message['text']}")

# Start listening continuously when button is clicked
if st.button("Start Listening"):
    st.write("👂 Listening... Speak continuously to interact with the assistant.")
    
    while True:
        # Recognize speech continuously
        recognized_text = listen_for_input("🎙️ Say something (or 'stop' to quit):")
        
        if recognized_text == "stop":
            st.write("👋 Stopped listening.")
            break

        if recognized_text:
            # Append user message to the conversation history
            st.session_state.conversation_history.append({"role": "user", "text": recognized_text})

            # Generate a response based on the recognized text
            response = create_context(recognized_text)  # This can be dynamic logic for responses
            st.session_state.conversation_history.append({"role": "assistant", "text": response})

            # Display the conversation history (user input and assistant reply)
            display_conversation()

            # Speak the assistant's reply
            speak_text(response, voice_index=1, rate=150, volume=1.0)

        else:
            st.error("⚠️ I couldn't understand what you said. Please try again.")
