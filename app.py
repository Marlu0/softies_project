# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
import os
import datetime
import tkinter as tk
from tkinter import filedialog
import threading # Import threading for running Flask in a separate thread
import webview # Import pywebview
from werkzeug.utils import secure_filename
from src.routes_api_keys import bp_api_keys
from src.speech2text import listen_for_input, listen_for_input_stream
from src.text2speech import speak_text
from src.chatbot_handler import chat_with_context
from src.api_handler import get_api_key, is_valid_api_key

# Corrected import for database.py, assuming it's in the 'src' subdirectory
from src.database import init_db, create_project, get_all_projects, get_project_by_id, delete_project, get_project_messages, get_project_id_by_name, get_blacklist_names, get_api_keys, create_project_message


app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here' # Keep this secret!

app.register_blueprint(bp_api_keys) #api key

# Initialize the database when the app starts
with app.app_context():
    init_db()

BASE_DIR = os.path.join(os.getcwd(), "projects")
os.makedirs(BASE_DIR, exist_ok=True)

# Allowed extenctions to upload
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.html', '.css', '.json', '.zip', '.pdf', '.xcsx', '.docx'}

BLACKLIST_FILE = 'blacklist.txt'

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return []
    with open(BLACKLIST_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def add_to_blacklist(filename):
    with open(BLACKLIST_FILE, 'a') as f:
        f.write(f"{filename}\n")

# --- Flask Routes (remain largely the same) ---

@app.route('/')
def home():
    projects = get_all_projects()
    return render_template('homepage.html', projects=projects)

@app.route('/create_project_page')
def create_project_page():
    flash('Project creation is handled by selecting a folder. Please click "Create new project" on the home page.', 'info')
    return redirect(url_for('home'))

@app.route("/chat/<project_name>")
def chat_project(project_name):
    projects = get_all_projects()
    project_id = get_project_id_by_name(project_name)

    if not project_id:
        return "Proyecto no encontrado", 404

    messages = get_project_messages(project_id)
    return render_template("chat.html", project_name=project_name, projects=projects, messages=messages)

@app.route("/chat/<project_name>/send", methods=["POST"])
def send_message(project_name):
    data = request.get_json()
    user_message = data.get("text")

    if not user_message:
        return jsonify({"error": "No message text provided"}), 400

    project_id = get_project_id_by_name(project_name)
    if not project_id:
        return jsonify({"error": "Invalid project name"}), 404

    create_project_message(project_id, user_message, sender="user")

    full_response = chat_with_context(folder_path=os.path.join(BASE_DIR, secure_filename(project_name)),
                                      user_prompt=user_message,
                                      is_first_prompt=False,
                                      model_name="gemini-2.0-flash",
                                      api_key=get_api_key())  # Replace with hardcoded API key if needed
    voice_text = full_response["speak_text"]
    chat_text = full_response["chat"]
    write_text = full_response["write"]

    bot_response = f"\"{chat_text}\""
    if speak_text:
        speak_text(voice_text)
    create_project_message(project_id, bot_response, sender="bot")

    return jsonify({"response": bot_response})

# NO LONGER A FLASK ROUTE ACCESSED DIRECTLY FROM JS FETCH
# @app.route('/select_project_folder', methods=['GET'])
# def select_project_folder():
# ...
# This functionality will be exposed directly via pywebview.
# We will remove this route and add a Python function exposed to JS.


@app.route('/add_selected_project', methods=['POST'])
def add_selected_project():
    data = request.get_json()
    project_path = data.get('path')

    if not project_path:
        return jsonify({'success': False, 'message': 'No folder path provided.'}), 400

    project_name = os.path.basename(project_path)
    
    # Validate project name
    if not project_name:
        return jsonify({'success': False, 'message': 'Invalid project name.'}), 400
    
    # Check if project path exists
    if not os.path.exists(project_path):
        return jsonify({'success': False, 'message': 'Selected folder does not exist.'}), 400

    # Check if it's a valid directory
    if not os.path.isdir(project_path):
        return jsonify({'success': False, 'message': 'Selected path is not a directory.'}), 400

    try:
        if create_project(project_name, project_path):
            flash(f'Project "{project_name}" added successfully!', 'success')
            return jsonify({'success': True, 'redirect_url': url_for('chat_project', project_name=project_name)})
        else:
            return jsonify({'success': False, 'message': 'A project with this name or path already exists.'}), 409
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating project: {str(e)}'}), 500


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project_route(project_id):
    project = get_project_by_id(project_id)
    if project:
        delete_project(project_id)
        flash(f'Project "{project["name"]}" removed successfully.', 'success')
        return jsonify({'success': True})
    else:
        flash('Project not found.', 'error')
        return jsonify({'success': False, 'message': 'Project not found.'}), 404
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_name = request.form.get('project_name', '').strip()
        if not project_name:
            flash('Please enter a project name.')
            return redirect(url_for('index'))

        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        folder_path = os.path.join(BASE_DIR, safe_name)

        try:
            os.makedirs(folder_path, exist_ok=False)
            flash(f'Project "{safe_name}" created successfully!')
        except FileExistsError:
            flash(f'Project "{safe_name}" already exists.')

        return redirect(url_for('upload', project=safe_name))

    return render_template('homepage.html')

@app.route('/upload/<project>', methods=['GET', 'POST'])
def upload(project):
    project_path = os.path.join(BASE_DIR, secure_filename(project))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)

        files = request.files.getlist('file')

        for file in files:
            if file and ALLOWED_EXTENSIONS(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(project_path, filename))
            else:
                flash(f'File "{file.filename}" is not allowed.')

        flash('Files uploaded successfully!')
        return redirect(request.url)

    return render_template('upload.html', project=project)

@app.route('/settings')
def settings():
    return render_template("settings.html",
                           blacklisted=get_blacklist_names(),
                           api_keys=get_api_keys())

@app.route('/blacklist', methods=['GET', 'POST'])
def blacklist():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            add_to_blacklist(filename)
        return redirect(url_for('blacklist'))

    blacklist_items = load_blacklist()
    return render_template('blacklist.html', blacklist=blacklist_items)

@app.route('/api/speech2text', methods=['POST'])
def api_speech2text():
    try:
        text = listen_for_input()
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech2text_stream', methods=['GET'])
def api_speech2text_stream():
    def event_stream():
        for partial in listen_for_input_stream():
            yield f"data: {partial}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/chat/<project_name>/send', methods=['POST'])
def chat_send(project_name):
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Empty message'}), 400
    project_id = get_project_id_by_name(project_name)
    if not project_id:
        return jsonify({'error': 'Project not found'}), 404
    # Store user message
    from src.database import create_project_message
    create_project_message(project_id, text, sender='user')
    # Dummy bot response (replace with real AI call if needed)
    bot_response = f"Echo: {text}"
    create_project_message(project_id, bot_response, sender='bot')
    return jsonify({'response': bot_response})

@app.route('/api/check_api_key')
def check_api_key():
    api_keys = get_api_keys()
    return jsonify({'has_key': len(api_keys) > 0})

@app.route('/api/api_keys/', methods=['POST'])
def add_api_key():
    data = request.get_json()
    name = data.get('name', '').strip()
    key = data.get('key', '').strip()

    if not key:
        return jsonify({'error': 'API key is required'}), 400
        
    if not key.startswith('sk-'):
        return jsonify({'error': 'Invalid API key format. OpenAI API keys should start with "sk-"'}), 400

    if len(key) < 20:
        return jsonify({'error': 'Invalid API key length. Please provide a valid OpenAI API key'}), 400

    try:
        # Here you would typically validate the key with OpenAI's API
        # For now, we'll just save it
        conn = get_db_connection()
        conn.execute('INSERT OR REPLACE INTO api_keys (name, key) VALUES (?, ?)', (name, key))
        conn.commit()
        conn.close()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to save API key: ' + str(e)}), 500

# --- Pywebview Integration ---

# Define a Python function to open the file dialog, exposed to JavaScript
class Api:
    def select_project_folder_dialog(self):
        # Tkinter needs to be run in the main thread for dialogs
        # When run via pywebview, this is usually the main thread
        root = tk.Tk()
        root.withdraw() # Hide the main Tkinter window
        folder_path = filedialog.askdirectory(title="Select Project Folder")
        root.destroy() # Destroy the Tkinter window after selection
        return folder_path # Return the path directly

api = Api() # Instantiate your API class

def start_flask():
    # Start the Flask app in a separate thread
    app.config['START_TIME'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False) # Important: debug=False, use_reloader=False when embedding

if __name__ == '__main__':
    # Start Flask in a separate thread
    t = threading.Thread(target=start_flask)
    t.daemon = True # Allow main program to exit even if thread is still running
    t.start()

    # Give Flask a moment to start up
    import time
    time.sleep(1)

    # Start pywebview window
    # The URL should match where your Flask app is running
    webview.create_window('Softy App', 'http://127.0.0.1:5000', js_api=api)
    webview.start()

    # If pywebview closes, Flask thread might still be active.
    # This is a simple shutdown for development. For production, more robust handling.
    print("Application closed.")

