import unittest
from flask import Flask
from main import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_autocomplete_success(self):
        response = self.app.get('/autocomplete', query_string={'term': 'Москва'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Москва', response.data)

    def test_autocomplete_empty_term(self):
        response = self.app.get('/autocomplete', query_string={'term': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_autocomplete_invalid_term(self):
        response = self.app.get('/autocomplete', query_string={'term': 'InvalidCity'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


if __name__ == '__main__':
    unittest.main()
