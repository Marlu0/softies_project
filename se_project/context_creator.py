import os
import openpyxl
import google.generativeai as genai

def create_context(folder_path):
    prompt = "You are an AI that understands the context of a folder based on its file contents.\n"
    prompt += "Here are the files and their contents:\n\n"
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    workbook = openpyxl.load_workbook(file_path)
                    content = ""
                    for sheet in workbook:
                        for row in sheet.iter_rows():
                            row_values = [str(cell.value) for cell in row]
                            content += ", ".join(row_values) + "\n"
                except Exception as e:
                    content = f"Error reading {file}: {e}"
            except Exception as e:
                content = f"Error reading {file}: {e}"
            prompt += f"--- {file_path} ---\n{content}\n\n"
    prompt += "What is the context of this folder?"
    return prompt

DEFAULT_API_KEY = "API_KEY_HERE"  # Replace with API key for gemini
DEFAULT_MODEL_NAME = "gemini-2.0-flash-001"

def chat_with_context(folder_path, user_prompt, api_key=DEFAULT_API_KEY, model_name=DEFAULT_MODEL_NAME):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)
    context = create_context(folder_path)
    full_prompt = f"{context}\n\nUser prompt: {user_prompt}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python context_creator.py <folder_path> <user_prompt>")
        sys.exit(1)
    folder_path = sys.argv[1]
    user_prompt = sys.argv[2]
    response = chat_with_context(folder_path, user_prompt)
    print(response)
