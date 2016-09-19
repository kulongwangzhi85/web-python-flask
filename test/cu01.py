#!/usr/bin/env python
# -*- coding:utf8 -*-

import sys
sys.path.append('..')

from app import db
from app.users import models
import unittest

class SQLALchemyTest(unittest.TestCase):
    """
    用于创建大量用户
    """
    def tearDown(self):
        db.session.remove()

    def test_createusers(self):
        for i in range(20):
            u = models.Users(username='guocl%02d' % i, email='guocl%02d@localhost.com' % i, password='aaaaaa')
            u.save()


if __name__ == '__main__':
    unittest.main()
