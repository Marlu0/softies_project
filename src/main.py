from speech2text import listen_for_input  # Function to transcribe live mic input
from chatbot_handler import chat_with_context  # Function to get Gemini AI output
from text2speech import speak_text  # Function to read text out loud
from api_handler import get_api_key #function to get or request the user the api key

FOLDER_PATH = "path_to_folder"

def main():
    api_key = get_api_key()
    while True:
        # 1. Listen to microphone until user says something (or "stop")
        user_input = listen_for_input()
        print(f"👨User said: {user_input}")
        if user_input.lower() == "stop":
            print("👋 Goodbye!")
            break

        # 2. Pass the transcribed text and folder to Gemini
        ai_response, modified_ai_response = chat_with_context(FOLDER_PATH, user_input, api_key)
        print(f"🤖AI Response: {ai_response}")

        # 3. Speak the AI response aloud
        speak_text(modified_ai_response)

if __name__ == "__main__":
    main()
