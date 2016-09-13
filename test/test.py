#!/usr/bin/env python

import sys
sys.path.append('..')

from app import db,app
from config import basedir
import unittest

class SQLALchemyTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/test/test.db' % basedir
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def test_post(self):
        print basedir


if __name__ == '__main__':
    unittest.main()
