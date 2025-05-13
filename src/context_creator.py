import os
import openpyxl
import google.generativeai as genai
import re

def remove_code_from_text(text):
    """
    Removes code snippets from the given text and replaces them with descriptions.
    """
    # Replace code blocks enclosed in triple backticks
    text = re.sub(r"```.*?```", "as shown in the code provided in the text box", text, flags=re.DOTALL)
    # Replace inline code enclosed in single backticks
    text = re.sub(r"`.*?`", "as shown in the code provided in the text box", text)
    return text

def create_context(folder_path):
    prompt = "You are an AI that understands the context of a folder based on its file contents.\n"
    prompt += "Here are the files and their contents:\n\n"
    file_contents = process_files(folder_path, "blacklist.txt")
    for file_path, content in file_contents.items():
        prompt += f"--- {file_path} ---\n{content}\n\n"
    prompt += "The previous text is the context for the next prompt:"
    return prompt

def process_files(folder_path, blacklist_file=os.path.join(os.path.dirname(__file__), "blacklist.txt")):
    file_contents = {}
    blacklist = []
    try:
        with open(blacklist_file, "r", encoding="utf-8") as f:
            for line in f:
                blacklist.append(os.path.normpath(line.strip()))
    except FileNotFoundError:
        print("Blacklist file not found. Continuing without blacklist.")

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))
            if file_path in blacklist:
                print(f"Skipping blacklisted file: {file_path}")
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents[file_path] = f.read()
            except UnicodeDecodeError:
                try:
                    workbook = openpyxl.load_workbook(file_path)
                    content = ""
                    for sheet in workbook:
                        for row in sheet.iter_rows():
                            row_values = [str(cell.value) for cell in row]
                            content += ", ".join(row_values) + "\n"
                    file_contents[file_path] = content
                except Exception as e:
                    file_contents[file_path] = f"Error reading {file}: {e}"
            except Exception as e:
                file_contents[file_path] = f"Error reading {file}: {e}"
    return file_contents

DEFAULT_API_KEY = "API_KEY_HERE"
DEFAULT_MODEL_NAME = "gemini-2.0-flash"

def chat_with_context(folder_path, user_prompt, api_key=DEFAULT_API_KEY, model_name=DEFAULT_MODEL_NAME):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)
    context = create_context(folder_path)
    full_prompt = f"{context}\n\nUser prompt: {user_prompt}"

    try:
        response = model.generate_content(full_prompt)
        original_response = response.text
        modified_response = remove_code_from_text(original_response)
        return original_response, modified_response
    except Exception as e:
        return f"Error generating response: {e}", f"Error generating response: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python context_creator.py <folder_path> <user_prompt>")
        sys.exit(1)
    folder_path = sys.argv[1]
    user_prompt = sys.argv[2]
    response = chat_with_context(folder_path, user_prompt)
    print(response)
