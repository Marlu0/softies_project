from speech2text import listen_for_input  # Function to transcribe live mic input
from context_creator import chat_with_context  # Function to get Gemini AI output
from text2speech import speak_text  # Function to read text out loud

FOLDER_PATH = "test_folder"

def main():
    while True:
        # 1. Listen to microphone until user says something (or "stop")
        user_input = listen_for_input()
        print(f"👨User said: {user_input}")
        if user_input.lower() == "stop":
            print("👋 Goodbye!")
            break

        # 2. Pass the transcribed text and folder to Gemini
        ai_response, modified_ai_response = chat_with_context(FOLDER_PATH, user_input)
        print(f"🤖AI Response: {ai_response}")

        # 3. Speak the AI response aloud
        speak_text(modified_ai_response)

if __name__ == "__main__":
    main()
