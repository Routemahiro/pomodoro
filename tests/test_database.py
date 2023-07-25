# tests/test_database.py
import os
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.database import DBHandler, init_db
import unittest
from model.database import DBHandler
from utils.text_generator import TextGenerator

class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db_handler = DBHandler()

    def test_create_connection(self):
        self.assertIsNotNone(self.db_handler.connection)

    def test_add_window_activity(self):
        session_id = 1
        time = '2023-07-19 12:00:00'
        window_name = 'Test Window'
        self.db_handler.add_window_activity(session_id, time, window_name)
        # Add assertions to check if the activity was correctly added to the database

    def test_get_activities(self):
        session_id = 1
        activities = self.db_handler.get_activities(session_id)
        # Add assertions to check if the returned activities are correct
        print(activities)

class TestTextGenerator(unittest.TestCase):
    def setUp(self):
        self.text_generator = TextGenerator()

    def test_generate_message(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
        response = self.text_generator.generate_message(messages)
        # Add assertions to check if the generated message is correct
        print(response)

if __name__ == '__main__':
    unittest.main()
