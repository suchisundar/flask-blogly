import unittest
from app import app, db
from models import User, Post

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///test_blogly"
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_homepage(self):
        """Test homepage route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recent Posts", response.data)

    def test_users_index(self):
        """Test users index route."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)

    def test_create_user(self):
        """Test creating a new user."""
        data = {'first_name': 'John', 'last_name': 'Doe', 'image_url': ''}
        response = self.client.post('/users/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User John Doe added.", response.data)

    def test_update_user(self):
        """Test updating an existing user."""
        user = User(first_name='John', last_name='Doe')
        db.session.add(user)
        db.session.commit()
        data = {'first_name': 'Jane', 'last_name': 'Doe', 'image_url': ''}
        response = self.client.post(f'/users/{user.id}/edit', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Jane Doe edited.", response.data)

    def test_posts_index(self):
        """Test posts index route."""
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 404)  # Assuming /posts route returns 404, modify as needed

    def test_create_post(self):
        """Test creating a new post."""
        user = User(first_name='John', last_name='Doe')
        db.session.add(user)
        db.session.commit()
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(f'/users/{user.id}/posts/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post 'Test Post' added.", response.data)

    

if __name__ == '__main__':
    unittest.main()
