import os
import openpyxl
import google.generativeai as genai
import re

# MACROS
DEFAULT_MODEL_NAME = "gemini-2.0-flash"

def remove_code_from_text(text):
    """
    Removes code snippets from the given text and replaces them with descriptions.
    This function processes the AI's output, not the input to the AI.
    """
    # Replace code blocks enclosed in triple backticks
    text = re.sub(r"```.*?```", "as shown in the code provided in the text box", text, flags=re.DOTALL)
    # Replace inline code enclosed in single backticks
    text = re.sub(r"`.*?`", "as shown in the code provided in the text box", text)
    return text

def create_context(folder_path, is_first_prompt=False):
    """
    Creates a context string for the AI model using the contents of files in the specified folder.
    This context will be prepended to the user's prompt.
    """
    prompt = "You are an AI expert in code analysis and improvement called Softy. "
    if is_first_prompt:
        prompt += "This is the first time you're being prompted for this project. Introduce yourself. "
    prompt += "You will act friendly, and provide technical but easy to understand insights when asked. Below is the content of several files from a project.\n"
    prompt += "Use this information as context to analyze, explain, correct, or improve code, according to the specific request in the following prompt provided by the user.\n\n"
    prompt += "File Contents:\n\n"

    file_contents = process_files(folder_path) # Call process_files to get file content

    # Add file contents to the prompt
    if not file_contents:
        prompt += "No readable text or code files found in the specified folder.\n\n"
    else:
        for file_path, content in file_contents.items():
            prompt += f"--- {file_path} ---\n{content}\n\n"

    prompt += "The response should be structured as follows:\n --SPEAK--\n<spoken content>\n--TEXT--\n<content that should be written in the chat with the AI>\n--WRITE--\n<code changes or suggestions>\n"
    prompt += "The following user prompt will contain the specific instructions for the code analysis:"
    return prompt

def process_files(folder_path, blacklist_file=os.path.join(os.path.dirname(__file__), "..", "data", "blacklist.txt")):
    """
    Processes files in the given folder, reading their contents.
    It identifies and reads common text/code files and Excel files.
    Files on the blacklist are skipped.
    """
    file_contents = {}
    blacklist = []

    # Load blacklist
    try:
        with open(blacklist_file, "r", encoding="utf-8") as f:
            for line in f:
                blacklist.append(os.path.normpath(line.strip()))
    except FileNotFoundError:
        print(f"Warning: Blacklist file '{blacklist_file}' not found. Continuing without blacklist.")
    except Exception as e:
        print(f"Error loading blacklist file: {e}. Continuing without blacklist.")

    # Define common text and code file extensions
    TEXT_CODE_EXTENSIONS = (
        '.py', '.js', '.html', '.css', '.txt', '.md', '.json', '.xml', '.yml', '.yaml',
        '.c', '.cpp', '.h', '.java', '.sh', '.bat', '.ps1', '.csv', '.log', '.go', '.rb',
        '.php', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.vue', '.svelte', '.toml',
        '.ini', '.cfg', '.conf', '.env', '.dockerfile', '.gitignore', '.editorconfig',
        '.prettierrc', '.eslintrc', '.webpack', '.babelrc', '.npmrc', '.yarnrc',
        '.gitmodules', '.gitattributes', '.gitkeep', '.project', '.classpath', '.settings',
        '.factorypath', '.buildpath', '.component', '.page', '.trigger', '.cls', '.cmp',
        '.app', '.resource', '.labels', '.object', '.field', '.layout', '.tab', '.flow',
        '.workflow', '.profile', '.permission', '.queue', '.sharingrules', '.role',
        '.site', '.community', '.dashboard', '.report', '.email', '.letterhead',
        '.document', '.folder', '.weblink', '.sitemap', '.robots', '.htaccess', '.htpasswd',
        '.npmignore', '.yarnignore', '.eslintignore', '.prettierignore', '.stylelintignore'
    )
    EXCEL_EXTENSIONS = ('.xlsx', '.xls', '.xlsm') # Added .xlsm for macro-enabled workbooks

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))

            if file_path in blacklist:
                print(f"Skipping blacklisted file: {file_path}")
                continue

            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in TEXT_CODE_EXTENSIONS:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents[file_path] = f.read()
                except UnicodeDecodeError:
                    print(f"Skipping binary or non-UTF-8 encoded text file: {file_path}")
                except Exception as e:
                    print(f"Error reading text/code file {file_path}: {e}")
                    file_contents[file_path] = f"Error reading {file}: {e}"
            elif file_extension in EXCEL_EXTENSIONS:
                try:
                    workbook = openpyxl.load_workbook(file_path)
                    content = ""
                    for sheet in workbook:
                        # Read cell values, handling potential None values
                        for row in sheet.iter_rows():
                            row_values = [str(cell.value) if cell.value is not None else "" for cell in row]
                            content += ", ".join(row_values) + "\n"
                    file_contents[file_path] = content
                except Exception as e:
                    print(f"Error reading Excel file {file_path}: {e}")
                    file_contents[file_path] = f"Error reading {file}: {e}"
            else:
                # Skip files with unsupported extensions without adding an error to the context
                print(f"Skipping unsupported file type: {file_path}")

    return file_contents

def chat_with_context(folder_path, user_prompt, api_key, is_first_prompt=False, model_name=DEFAULT_MODEL_NAME):
    """
    Interacts with the AI model using the generated context and the user's prompt.
    Returns both the original response from the AI and a modified version with code snippets replaced.
    """
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)
    context = create_context(folder_path, is_first_prompt)
    full_prompt = f"{context}\n\nUser prompt: {user_prompt}"

    print("\n--- Full Prompt Sent to Model ---")
    print(full_prompt) # Print the full prompt for debugging/verification
    print("---------------------------------\n")

    try:
        response = model.generate_content(full_prompt)
        original_response = response.text
        modified_response = remove_code_from_text(original_response)
        parts = re.split(r'--SPEAK--\n|--TEXT--\n|--WRITE--\n', modified_response, flags=re.DOTALL)
        speak_text = parts[1].strip() if len(parts) > 1 else ""
        chat = parts[2].strip() if len(parts) > 2 else ""
        write = parts[3].strip() if len(parts) > 3 else ""
        return {"speak_text": speak_text, "chat": chat, "write": write}
    except Exception as e:
        return {"speak_text": "", "chat": f"Error generating response: {e}", "write": ""}
