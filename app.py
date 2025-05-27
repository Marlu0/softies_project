# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import datetime
import tkinter as tk
from tkinter import filedialog
import json
import threading # Import threading for running Flask in a separate thread
import webview # Import pywebview
from werkzeug.utils import secure_filename

# Corrected import for database.py, assuming it's in the 'src' subdirectory
from src.database import init_db, create_project, get_project_names, get_project_path, delete_project, get_project_messages


app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here' # Keep this secret!

# Initialize the database when the app starts
with app.app_context():
    init_db()

BASE_DIR = os.path.join(os.getcwd(), "projects")
os.makedirs(BASE_DIR, exist_ok=True)

# Allowed extenctions to upload
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.html', '.css', '.json', '.zip', '.pdf', '.xcsx', '.docx'}

BLACKLIST_PATH = 'blacklist.json'

def load_blacklist():
    if os.path.exists(BLACKLIST_PATH):
        with open(BLACKLIST_PATH) as f:
            return json.load(f)
    return []

def save_blacklist(files):
    with open(BLACKLIST_PATH, 'w') as f:
        json.dump(files, f)

# --- Flask Routes (remain largely the same) ---

@app.route('/')
def home():
    projects = get_project_names()
    return render_template('homepage.html', projects=projects)

@app.route('/create_project_page')
def create_project_page():
    flash('Project creation is handled by selecting a folder. Please click "Create new project" on the home page.', 'info')
    return redirect(url_for('home'))

@app.route("/chat/<project_name>")
def chat_project(project_name):
    projects = get_project_names()
    project_id = get_project_id_by_name(project_name)

    if not project_id:
        return "Proyecto no encontrado", 404

    messages = get_project_messages(project_id)
    return render_template("chat.html", project_name=project_name, projects=projects, messages=messages)


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

    if create_project(project_name, project_path):
        flash(f'Project "{project_name}" added successfully!', 'success')
        return jsonify({'success': True, 'redirect_url': url_for('home')})
    else:
        flash(f'A project with name "{project_name}" or path "{project_path}" already exists.', 'warning')
        return jsonify({'success': False, 'message': 'Project already exists.'}), 409


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project_route(project_id):
    project = get_project_path(project_id)
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
    blacklisted = load_blacklist()
    return render_template('settings.html')

@app.route('/blacklist', methods=['POST'])
def blacklist_files():
    files = request.files.getlist('blacklist_files')
    blacklist = load_blacklist()

    for file in files:
        filename = file.filename
        if filename and filename not in blacklist:
            blacklist.append(filename)

    save_blacklist(blacklist)
    return redirect(url_for('settings'))

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