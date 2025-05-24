import unittest
import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import database
from src.database import get_db_connection, init_db, create_project, get_project_names, get_project_path, delete_project, create_api_key, get_api_keys, delete_api_key, update_api_key, create_blacklist_record, get_blacklist_names, get_blacklist_path, delete_blacklist_record, update_project_context_summary, get_project_messages

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Setup a test database
        self.test_db = 'test_softy_projects.db'
        database.DATABASE = self.test_db
        init_db()
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Clean up the test database
        self.conn.close()
        os.remove(self.test_db)

    def test_create_and_get_project(self):
        project_name = "Test Project"
        project_path = "/path/to/test/project"
        create_project(project_name, project_path)
        names = get_project_names()
        self.assertIn(project_name, names)
        project_id = self.cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,)).fetchone()[0]
        path = get_project_path(project_id)
        self.assertEqual(path, project_path)

    def test_create_and_get_api_key(self):
        api_key_name = "test_api"
        api_key_value = "test_key"
        create_api_key(api_key_name, api_key_value)
        keys = get_api_keys()
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0]['name'], api_key_name)
        self.assertEqual(keys[0]['key'], api_key_value)

    def test_delete_project(self):
        project_name = "ToDelete"
        project_path = "/path/to/delete"
        create_project(project_name, project_path)
        project_id = self.cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,)).fetchone()[0]
        delete_project(project_id)
        names = get_project_names()
        self.assertNotIn(project_name, names)

    def test_delete_api_key(self):
        api_key_name = "delete_api"
        api_key_value = "delete_key"
        create_api_key(api_key_name, api_key_value)
        delete_api_key(api_key_name)
        keys = get_api_keys()
        self.assertEqual(len(keys), 0)

    def test_update_api_key(self):
        api_key_name = "update_api"
        api_key_value = "old_key"
        create_api_key(api_key_name, api_key_value)
        new_api_key_value = "new_key"
        update_api_key(api_key_name, new_api_key_value)
        keys = get_api_keys()
        self.assertEqual(keys[0]['key'], new_api_key_value)

    def test_create_and_get_blacklist_record(self):
        record_type = "file"
        record_name = "test_file"
        record_path = "/path/to/file"
        create_blacklist_record(record_type, record_name, record_path)
        names = get_blacklist_names()
        self.assertIn(record_name, names)
        record_id = self.cursor.execute("SELECT id FROM blacklist WHERE name = ?", (record_name,)).fetchone()[0]
        path = get_blacklist_path(record_id)
        self.assertEqual(path, record_path)

    def test_delete_blacklist_record(self):
        record_type = "file"
        record_name = "delete_file"
        record_path = "/path/to/delete_file"
        create_blacklist_record(record_type, record_name, record_path)
        record_id = self.cursor.execute("SELECT id FROM blacklist WHERE name = ?", (record_name,)).fetchone()[0]
        delete_blacklist_record(record_id)
        names = get_blacklist_names()
        self.assertNotIn(record_name, names)

    def test_update_project_context_summary(self):
        project_name = "ContextProject"
        project_path = "/path/to/context/project"
        create_project(project_name, project_path)
        project_id = self.cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,)).fetchone()[0]
        new_summary = "This is an updated context summary."
        update_project_context_summary(project_id, new_summary)
        self.cursor.execute("SELECT context_summary FROM projects WHERE id = ?", (project_id,))
        summary = self.cursor.fetchone()[0]
        self.assertEqual(summary, new_summary)

    def test_get_project_messages(self):
        project_name = "MessageProject"
        project_path = "/path/to/message/project"
        create_project(project_name, project_path)
        project_id = self.cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,)).fetchone()[0]
        messages = get_project_messages(project_id)
        self.assertEqual(len(messages), 0)

if __name__ == '__main__':
    unittest.main()
