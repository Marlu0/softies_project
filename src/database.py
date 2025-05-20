# src/database.py
import sqlite3
import os

# Determine the absolute path to the root directory (softy_app/)
# This assumes database.py is in softy_app/src/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data') # Path to the data directory

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Database file will be inside the 'data' directory
DATABASE = os.path.join(DATA_DIR, 'softy_projects.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # This allows access to columns by name
    return conn

def init_db():
    """Initializes the database schema (creates the projects table if it doesn't exist)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            path TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_project(name, path):
    """Adds a new project to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO projects (name, path) VALUES (?, ?)", (name, path))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This means a project with that name or path already exists
        return False
    finally:
        conn.close()

def get_projects():
    """Retrieves all projects from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, path FROM projects ORDER BY name ASC")
    projects = cursor.fetchall()
    conn.close()
    # Convert Row objects to dictionaries for easier handling in Flask
    return [dict(project) for project in projects]

def get_project_by_id(project_id):
    """Retrieves a single project by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, path FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    conn.close()
    return dict(project) if project else None

def delete_project(project_id):
    """Deletes a project from the database by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database initialized or already exists at: {DATABASE}")