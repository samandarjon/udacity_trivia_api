import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from backend.flaskr import create_app
from backend.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "db_trivia"
        self.database_path = "postgresql://postgres:smndr2013@{}/{}" \
            .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""

    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)

        cats = res.json
        self.assertTrue(cats['categories'])
        self.assertTrue(cats['categories'][0])
        self.assertTrue(cats['categories'][0]['id'])
        self.assertTrue(cats['categories'][0]['type'])

        with self.assertRaises(KeyError):
            var = cats['categories'][0]['name']

        with self.assertRaises(IndexError):
            var = cats['categories'][1000000]

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

        q = res.json
        self.assertIsNotNone(q)
        self.assertGreater(q.__len__(), 0)

        self.assertIn('questions', q)
        self.assertIn('total_questions', q)
        self.assertIn('categories', q)
        self.assertIn('current_category', q)

        with self.assertRaises(KeyError):
            var = q['blah']

        with self.assertRaises(KeyError):
            var = q[1000000]

    def test_add_question(self):
        q = {
            'question': 'q1',
            'answer': 'a1',
            'difficulty': '1',
            'category': 1
        }

        res = self.client().post('/add-questions', json=q)
        self.assertTrue(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_delete_question_by_id(self):
        questions = self.client().get('/questions')

        data = json.loads(questions.data)

        original_length = len(questions.json)
        self.assertGreater(original_length, 0)

        id_to_delete = data['questions'][original_length]['id']
        questions_deleted = self.client().delete('/questions/' +
                                                 str(id_to_delete))

        new_length = len(questions_deleted.json)
        self.assertGreater(original_length, new_length)

    def test_search_questions(self):
        search_term = {
            'searchTerm': 'e'
        }
        res = self.client().post('/search-questions', json=search_term)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreater(len(data), 0)


if __name__ == "__main__":
    unittest.main()
