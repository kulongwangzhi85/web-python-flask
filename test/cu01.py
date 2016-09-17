#!/usr/bin/env python

import sys
sys.path.append('..')

from app import db
from app.users import models
import unittest

class SQLALchemyTest(unittest.TestCase):

    def tearDown(self):
        db.session.remove()

    def test_createusers(self):
        for i in range(20):
            u = models.Users(username='guocl%02d' % i, email='guocl%02d@localhost.com' % i, password='aaaaaa')
            u.save()


if __name__ == '__main__':
    unittest.main()
