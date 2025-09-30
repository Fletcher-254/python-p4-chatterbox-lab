from datetime import datetime
from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

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
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        with app.app_context():
            msg = Message(body="Hello 👋", username="Liza")
            db.session.add(msg)
            db.session.commit()

            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert message['id'] in [record.id for record in records]
                assert message['body'] in [record.body for record in records]

    def test_creates_new_message_in_the_database(self):
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={"body": "Hello 👋", "username": "Liza"}
            )

            msg = Message.query.filter_by(body="Hello 👋").first()
            assert msg

    def test_returns_data_for_newly_created_message_as_json(self):
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={"body": "Hello 👋", "username": "Liza"}
            )

            assert response.content_type == 'application/json'
            assert response.json["body"] == "Hello 👋"
            assert response.json["username"] == "Liza"

    def test_updates_body_of_message_in_database(self):
        with app.app_context():
            msg = Message(body="Hello 👋", username="Liza")
            db.session.add(msg)
            db.session.commit()

            response = app.test_client().patch(
                f'/messages/{msg.id}',
                json={"body": "Goodbye 👋"}
            )

            updated = Message.query.get(msg.id)
            assert updated.body == "Goodbye 👋"

    def test_returns_data_for_updated_message_as_json(self):
        with app.app_context():
            msg = Message(body="Hello 👋", username="Liza")
            db.session.add(msg)
            db.session.commit()

            response = app.test_client().patch(
                f'/messages/{msg.id}',
                json={"body": "Goodbye 👋"}
            )

            assert response.content_type == 'application/json'
            assert response.json["body"] == "Goodbye 👋"

    def test_deletes_message_from_database(self):
        with app.app_context():
            msg = Message(body="Hello 👋", username="Liza")
            db.session.add(msg)
            db.session.commit()

            app.test_client().delete(f'/messages/{msg.id}')

            deleted = Message.query.get(msg.id)
            assert deleted is None
