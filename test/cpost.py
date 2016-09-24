#!/usr/bin/env python
# -*- coding:utf8 -*-

import sys
sys.path.append('..')

from app import db
from app.common import models
import unittest

class SQLALchemyTest(unittest.TestCase):
    """
    创建大量文章,用于测试翻页功能的编写
    """
    def tearDown(self):
        db.session.remove()

    def test_createusers(self):
        for i in range(100):
            a = models.Post.query.get(1)
            u = models.Post(name=a.name+'%02d' % i)
            u.category = a.category
            u.container = a.container
            u.author = a.author
            u.small = a.small
            u.save()


if __name__ == '__main__':
    unittest.main()
