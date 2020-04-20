from unittest import TestCase

from app import app
from models import db, User, Post

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

        db.create_all()
        user = User(first_name="Test", last_name="Case", image_url="https://google.com")
        
        db.session.add(user)
        db.session.commit()

        post = Post(title="Testingtitle", content="Hope this works", user_id=1)

        db.session.add(post)
        db.session.commit()
        self.user_id = user.id
    
    def tearDown(self):
        """Clean up"""
        db.session.remove()
        db.drop_all()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Case', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Test Case</h2>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "Joe", "last-name": "Smith", "img-url": "http://google.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Joe Smith", html)

    def test_outofrange_user(self):
        with app.test_client() as client:
            resp = client.get("/users/1035829351")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 404)
            self.assertIn("<p>What you were looking for is just not there.</p>", html)
    
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Test123", "content":"Is this on?", "user_id":"1"}
            resp = client.post("users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test123", html)

    def test_delete_post(self):
        with app.test_client() as client:
            d = {"title":"Testingtitle", "content":"Hope this works", "user_id":"1"}
            resp = client.post("posts/1/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Testingtitle", html)

    
            