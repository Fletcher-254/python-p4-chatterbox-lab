from datetime import datetime
from app import app
from models import db, Message

class TestMessage:
    '''Message model in models.py'''

    @staticmethod
    def clear_messages():
        with app.app_context():
            for message in Message.query.all():
                db.session.delete(message)
            db.session.commit()

    def setup_method(self):
        """Run before each test to ensure clean DB."""
        self.clear_messages()

    def teardown_method(self):
        """Run after each test to clean DB."""
        self.clear_messages()

    def test_has_correct_columns(self):
        '''Has columns for message body, username, and creation time.'''
        with app.app_context():
            hello_from_liza = Message(body="Hello 👋", username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)
