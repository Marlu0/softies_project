# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
# Add a secret key for flash messages (important for production apps)
# For a simple local app, a hardcoded key is fine, but for production,
# consider using environment variables or a more secure method.
app.secret_key = 'your_super_secret_key_here'

# --- Configuration (You can expand this later) ---
# Example: Directory to store project data
PROJECTS_DIR = 'projects'
if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# --- Routes ---

@app.route('/')
def home():
    """
    Renders the home screen (index.html).
    You could potentially load existing projects here to display them.
    """
    # For now, let's just render the template.
    # In a real app, you might fetch a list of projects from a database or file system
    # and pass them to the template:
    # existing_projects = get_list_of_projects_from_somewhere()
    # return render_template('index.html', projects=existing_projects)
    return render_template('index.html')

@app.route('/create_project_page')
def create_project_page():
    """
    Renders the create new project screen (create_project.html).
    """
    return render_template('create_project.html')

@app.route('/submit_project', methods=['POST'])
def submit_project():
    """
    Handles the form submission for creating a new project.
    """
    project_name = request.form.get('projectName')

    if not project_name:
        flash('Project name cannot be empty!', 'error')
        return redirect(url_for('create_project_page')) # Redirect back to the form

    # Sanitize the project name for file system use (basic example)
    safe_project_name = "".join(c for c in project_name if c.isalnum() or c in [' ', '_']).strip()
    safe_project_name = safe_project_name.replace(' ', '_')

    # Check if a project with this name already exists
    project_path = os.path.join(PROJECTS_DIR, safe_project_name)
    if os.path.exists(project_path):
        flash(f'A project named "{project_name}" already exists. Please choose a different name.', 'warning')
        return redirect(url_for('create_project_page'))

    try:
        # Create a directory for the new project
        os.makedirs(project_path)
        # You can also create initial files here, e.g., a config file for the project
        with open(os.path.join(project_path, 'project_info.txt'), 'w') as f:
            f.write(f"Project Name: {project_name}\n")
            f.write(f"Created On: {app.config['START_TIME']}\n") # Example of using a global config

        flash(f'Project "{project_name}" created successfully!', 'success')
        print(f"DEBUG: New project directory created at {project_path}")
        # Redirect to the home page or a specific project details page
        return redirect(url_for('home'))

    except OSError as e:
        flash(f'Error creating project: {e}', 'error')
        print(f"ERROR: Could not create project directory: {e}")
        return redirect(url_for('create_project_page'))

# --- Main Application Runner ---

if __name__ == '__main__':
    # Set a start time for potential use in project creation
    import datetime
    app.config['START_TIME'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # When debug is True:
    # 1. The server will reload automatically on code changes.
    # 2. A debugger will be active in the browser for server-side errors.
    # IMPORTANT: Set debug=False in production environments.
    app.run(debug=True, port=5000) # You can change the port if 5000 is in use