# src/database.py
import sqlite3
import os

# Database file is now in the same directory as this script (src/)
DATABASE = 'softy_projects.db'

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
    # This block runs when you execute database.py directly,
    # useful for initial setup or testing.
    init_db()
    print("Database initialized or already exists.")
    # Example usage:
    # add_project("My First Project", "/home/user/my_project_1")
    # add_project("Another App", "C:\\Users\\user\\Documents\\another_app")
    # projects = get_projects()
    # for p in projects:
    #     print(p)