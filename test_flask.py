from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Test", last_name="Case", image_url="https://google.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Test Case</h2>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Joe", "last_name": "Smith", "image_url": "http://google.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Joe Smith", html)

    def test_outofrange_user(self):
        with app.test_client() as client:
            resp = client.get("/users/1035829351")

            self.assertEqual(resp.status_code, 404)
            