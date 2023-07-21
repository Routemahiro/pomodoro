import unittest
from db_handler import DBHandler

class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db_handler = DBHandler('tests/data/test.db')

    def tearDown(self):
        self.db_handler.close_connection()

    def test_insert_session(self):
        session_id = self.db_handler.start_session()
        self.assertIsNotNone(session_id)

    def test_get_session(self):
        session_id = self.db_handler.start_session()
        session = self.db_handler.get_session(session_id)
        self.assertIsNotNone(session)

    def test_update_session(self):
        session_id = self.db_handler.start_session()
        self.db_handler.end_session(session_id)
        session = self.db_handler.get_session(session_id)
        self.assertIsNotNone(session['end_time'])

    def test_delete_session(self):
        session_id = self.db_handler.start_session()
        self.db_handler.delete_session(session_id)
        session = self.db_handler.get_session(session_id)
        self.assertIsNone(session)

if __name__ == "__main__":
    unittest.main()