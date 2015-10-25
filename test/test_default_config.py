# -*- coding: utf-8 -*-
import unittest
from todotxt_web import default_config


class TestDefaultConifg(unittest.TestCase):

    def test_default_confg(self):
        self.assertTrue(hasattr(default_config, 'port'), msg="Port is not defined")
        self.assertTrue(hasattr(default_config, 'todo_file'), msg="todo_file is not defined")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
