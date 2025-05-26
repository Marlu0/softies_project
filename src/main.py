import os
import re

from speech2text import listen_for_input  # Function to transcribe live mic input
from chatbot_handler import chat_with_context  # Function to get Gemini AI output
from text2speech import speak_text  # Function to read text out loud
from api_handler import get_api_key #function to get or request the user the api key

FOLDER_PATH = "C:/Users/marce/Documents/Code/softies_project/test/test_project"

def main():
    """
    Main function to run the AI assistant.
    It listens for user input, sends it to the AI with context,
    speaks the AI's response, and handles potential code writing.
    """
    api_key = get_api_key()
    if api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("Warning: Please set your GEMINI_API_KEY environment variable or replace 'YOUR_GEMINI_API_KEY_HERE' with your actual API key.")

    while True:
        # 1. Listen to microphone until user says something (or "stop")
        user_input = listen_for_input()
        print(f"👨User said: {user_input}")
        if user_input.lower() == "stop":
            print("👋 Goodbye!")
            break

        # 2. Pass the transcribed text and folder to Gemini
        # The chat_with_context function returns a single formatted string
        ai_response_tuple, full_ai_response_str = chat_with_context(FOLDER_PATH, user_input, api_key)

        print(full_ai_response_str)
        # 3. Parse the AI response string into its components
        # Split the string by the markers --SPEAK--, --TEXT--, --WRITE--
        # re.split keeps the delimiters if they are captured in a group, but here we just want the content
        parts = re.split(r'--SPEAK--\n|--TEXT--\n|--WRITE--\n', full_ai_response_str, flags=re.DOTALL)

        # The parts list will typically contain ['', speak_content, text_content, write_content]
        # We need to handle cases where a section might be empty or missing.
        # The first element is usually empty due to the split at the beginning.
        speak_content = parts[1].strip() if len(parts) > 1 else ""
        text_content = parts[2].strip() if len(parts) > 2 else ""
        write_content = parts[3].strip() if len(parts) > 3 else ""

        print(f"\n--- AI Response (Full Text) ---\n{text_content}\n-------------------------------\n")

        # 4. Speak the AI response aloud (using the --SPEAK-- content)
        if speak_content:
            speak_text(speak_content)
        else:
            print("No spoken content from AI response.")

        # 5. Handle code writing (using the --WRITE-- content)
        if write_content and write_content != "// No code changes suggested.":
            print("\n--- AI Suggested Code Changes ---")
            # Iterate through suggested file paths and code blocks
            write_lines = write_content.split('\n')
            current_obj_path = None
            current_code_block = []
            for line in write_lines:
                if line.startswith("ObjPath:"):
                    # If we have a previous block, process it before starting a new one
                    if current_obj_path and current_code_block:
                        print(f"Writing to: {current_obj_path}")
                        # Join the code lines and remove leading/trailing whitespace
                        code_to_write = ''.join(current_code_block).strip()
                        print(f"Code:\n{code_to_write}")
                        # In a real application, you would write this to a file:
                        # with open(current_obj_path, 'w', encoding='utf-8') as f:
                        #     f.write(code_to_write)
                        print("-" * 30) # Separator for multiple code blocks

                    # Start a new code block
                    current_obj_path = line.replace("ObjPath:", "").strip()
                    current_code_block = []
                elif current_obj_path is not None:
                    # Append lines to the current code block
                    current_code_block.append(line + '\n')
            
            # Process the last code block after the loop finishes
            if current_obj_path and current_code_block:
                print(f"Writing to: {current_obj_path}")
                code_to_write = ''.join(current_code_block).strip()
                print(f"Code:\n{code_to_write}")
                # In a real application, you would write this to a file:
                # with open(current_obj_path, 'w', encoding='utf-8') as f:
                #     f.write(code_to_write)
                print("-" * 30) # Separator for multiple code blocks

            print("---------------------------------\n")
        else:
            print("\n// No code changes suggested by AI.\n")


if __name__ == "__main__":
    main()
