# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import datetime
import tkinter as tk
from tkinter import filedialog
import json
import threading # Import threading for running Flask in a separate thread
import webview # Import pywebview

# Corrected import for database.py, assuming it's in the 'src' subdirectory
from src.database import init_db, add_project, get_projects, get_project_by_id, delete_project

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here' # Keep this secret!

# Initialize the database when the app starts
with app.app_context():
    init_db()

# --- Flask Routes (remain largely the same) ---

@app.route('/')
def home():
    projects = get_projects()
    return render_template('index.html', projects=projects)

@app.route('/create_project_page')
def create_project_page():
    flash('Project creation is handled by selecting a folder. Please click "Create new project" on the home page.', 'info')
    return redirect(url_for('home'))

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

    if add_project(project_name, project_path):
        flash(f'Project "{project_name}" added successfully!', 'success')
        return jsonify({'success': True, 'redirect_url': url_for('home')})
    else:
        flash(f'A project with name "{project_name}" or path "{project_path}" already exists.', 'warning')
        return jsonify({'success': False, 'message': 'Project already exists.'}), 409


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