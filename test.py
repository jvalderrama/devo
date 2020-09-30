#!/usr/bin/env python
import unittest
import app

class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_check_devo_ok(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'OK\n')

    def test_check_devo_ko(self):
        rv = self.app.get('/')
        self.assertRaises(Exception, b'KO\n')


if __name__ == '__main__':
    unittest.main()
