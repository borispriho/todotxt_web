# -*- coding: utf-8 -*-
"""Testing main page of application"""

import os

from tornado.options import options
from tornado.testing import AsyncHTTPTestCase

from todotxt_web import server

APP = server.make_app()
options.parse_config_file(os.path.join('test', 'config.py'))


class TestHandlerBase(AsyncHTTPTestCase):
    """TestCase with initialized app"""

    def get_app(self):
        return APP      # this is the global app that we created above.


class TestTodoTxtWebMainPage(TestHandlerBase):

    def setUp(self):
        super(TestHandlerBase, self).setUp()
        """Fetch main page to self.page"""
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.page = response.buffer.read()

    def test_main_page(self):
        self.assertIn('todo.txt', self.page)


    def test_includes(self):
        """Testing including js/css"""
        self.assertIn('material.min.css', self.page)
        self.assertIn('material.min.js', self.page)
        self.assertIn('icon.css', self.page)
        self.assertIn('viewport', self.page)
        self.assertIn('main.css', self.page)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
