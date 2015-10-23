# -*- coding: utf-8 -*-
"""Testing main page of application"""

import os

from tornado.options import options
from tornado.testing import AsyncHTTPTestCase

from todotxt_web import server

APP = server.make_app()
options.parse_config_file(os.path.join('test', 'config.py'))


class TestHandlerBase(AsyncHTTPTestCase):

    def get_app(self):
        return APP      # this is the global app that we created above.


class TestDevWorkerMainPage(TestHandlerBase):

    def test_main_page(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        page = response.buffer.read()
        self.assertIn('todo.txt', page)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
