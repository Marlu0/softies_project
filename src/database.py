import sqlite3
import os

# Determine the absolute path to the root directory (softy_app/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATABASE = os.path.join(DATA_DIR, 'softy_projects.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR NOT NULL UNIQUE,
        path VARCHAR NOT NULL UNIQUE,
        context_summary TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        time DATETIME DEFAULT CURRENT_TIMESTAMP,
        project INTEGER,
        sender VARCHAR,
        FOREIGN KEY(project) REFERENCES projects(id)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR,
        name VARCHAR,
        path VARCHAR
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS api_keys (
        name VARCHAR PRIMARY KEY,
        key VARCHAR
    )""")

    conn.commit()
    conn.close()

# Create operations
def create_project(name, path, context_summary=None):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO projects (name, path, context_summary) VALUES (?, ?, ?)", (name, path, context_summary))
        conn.commit()
    finally:
        conn.close()

def create_project_message(project_id, text, sender='USER'):
    """Creates a chat message for a given project with the current timestamp."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO chat_messages (text, time, project, sender)
            VALUES (?, datetime('now'), ?, ?)
        """, (text, project_id, sender))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Invalid project ID or other DB constraint issue
        return False
    finally:
        conn.close()

def create_api_key(name, key):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO api_keys (name, key) VALUES (?, ?)", (name, key))
        conn.commit()
    finally:
        conn.close()

def create_blacklist_record(type_, name, path):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO blacklist (type, name, path) VALUES (?, ?, ?)", (type_, name, path))
        conn.commit()
    finally:
        conn.close()

# Read operations

def get_all_projects():
    conn = get_db_connection()
    projects = conn.execute("SELECT id, name FROM projects").fetchall()
    conn.close()
    return projects

def get_all_project_names():
    conn = get_db_connection()
    projects = conn.execute("SELECT name FROM projects").fetchall()
    conn.close()
    return projects

def get_project_by_id(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects where id = ?", (project_id,))
    project = cursor.fetchone()
    conn.close()
    return project

def get_project_id_by_name(project_name):
    """Returns the project ID for a given project name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
    result = cursor.fetchone()
    conn.close()
    return result["id"] if result else None

def get_blacklist_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM blacklist")
    names = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return names

def get_project_path(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    return row['path'] if row else None

def get_blacklist_path(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM blacklist WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row['path'] if row else None

def get_project_messages(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_messages WHERE project = ? ORDER BY time", (project_id,))
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return messages

def get_api_keys():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys")
    keys = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return keys

# Delete operations

def delete_project_messages(project_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM messages WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
    finally:
        conn.close()

def delete_api_key(name):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM api_keys WHERE name = ?", (name,))
        conn.commit()
    finally:
        conn.close()

def delete_blacklist_record(record_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM blacklist WHERE id = ?", (record_id,))
        conn.commit()
    finally:
        conn.close()

# Update operations
def update_api_key(name, new_key):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE api_keys SET key = ? WHERE name = ?", (new_key, name))
        conn.commit()
    finally:
        conn.close()

def update_project_context_summary(project_id, summary):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE projects SET context_summary = ? WHERE id = ?", (summary, project_id))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database initialized or already exists at: {DATABASE}")
