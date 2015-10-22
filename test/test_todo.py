# -*- coding: utf-8 -*-
"""Testing main todo_txt funnctionality"""

import unittest
import os

from todotxt_web import todo_txt

TXT_FILE = 'test/todo.txt'


class TestTodoTxt(unittest.TestCase):
    """Testing class TodoTxt"""

    def setUp(self):
        self.todo = todo_txt.TodoTxt(TXT_FILE)

    def tearDown(self):
        if os.path.exists(TXT_FILE):
            os.remove(TXT_FILE)
        if os.path.exists(TXT_FILE + todo_txt.BACKUP_EXT):
            os.remove(TXT_FILE + todo_txt.BACKUP_EXT)

    def test_todo_init(self):
        """test TodoTxt initialization"""
        self.assertIsInstance(self.todo, todo_txt.TodoTxt)
        self.assertEqual(self.todo.file_name, TXT_FILE)

    def test_add(self):
        """test adding new records to file"""
        record = "A sample todo record"
        self.todo.add(record)
        with open(self.todo.file_name) as todo_fh:
            self.assertIn(record, todo_fh.read(), msg="Record not found")

    def test_mark_complete(self):
        """test marking task as complete adding its begining 'x'
        letter
        """
        record = "A sample todo record for marking as done"
        self.todo.add(record)
        self.todo.done(record)
        with open(self.todo.file_name) as todo_fh:
            self.assertIn('x ' + record, todo_fh.read(), msg="Marked record not found")

    def test_clean(self):
        """Test clean() method which remove all records which marked as
        'done'
        """
        record1 = "A record which will be removed from todo.txt"
        record2 = "A seconf record which should be exists after cleaning of todo.txt"
        self.todo.add(record1)
        self.todo.add(record2)
        self.todo.done(record1)
        self.todo.clean()
        with open(self.todo.file_name) as todo_fh:
            self.assertNotIn('x ' + record1, todo_fh.read(),
                             msg="Marked record is not cleaned")
        with open(self.todo.file_name) as todo_fh:
            self.assertIn(record2, todo_fh.read(),
                          msg="The second record does not exist in todo.txt file")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
