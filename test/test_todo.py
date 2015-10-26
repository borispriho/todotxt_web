# -*- coding: utf-8 -*-
"""Testing main todo_txt functionality"""

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
        """test marking task as complete adding its beginning 'x'
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
        record2 = "A second record which should be exists after cleaning of todo.txt"
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

    def test_iter_todo(self):
        """Test __iter__ of todo object"""
        for line in self.todo:
            self.assertIsInstance(line, basestring)

    def test_serialize_line(self):
        """Test serializing text line to representing dictionary"""
        line = "Some text line"
        self.assertIn('line', self.todo.serialize_line(line))
        self.assertIn('done', self.todo.serialize_line(line))
        self.assertFalse(self.todo.serialize_line(line)['done'])
        self.assertTrue(self.todo.serialize_line('x ' + line)['done'])
        self.assertTrue(self.todo.serialize_line('x       ' + line)['done'])
        self.assertIn('projects', self.todo.serialize_line(line))
        self.assertIn('projects', self.todo.serialize_line(line + ' +project_1'))
        self.assertIn('+project_1', self.todo.serialize_line(line + ' +project_1')['projects'])
        self.assertEqual(len(self.todo.serialize_line(line +
                                                      ' +project_1 +project_2')['projects']), 2)
        self.assertIn('contexts', self.todo.serialize_line(line))
        self.assertIn('@home', self.todo.serialize_line(line + ' @home')['contexts'])
        self.assertEqual(len(self.todo.serialize_line(line +
                                                      ' @home @work')['contexts']), 2)

    def test_serialize(self):
        """Test serialize todo object"""
        self.todo.add("The record 1")
        self.todo.add("The record 2")
        serialized_todo = self.todo.serialize()
        self.assertIsInstance(serialized_todo, list)
        first_line = serialized_todo[0]
        self.assertIsInstance(first_line, dict)

    def test_unserialize_line(self):
        line_dict = {'done': True, 'line': 'Text of line',
                     'contexts': ['@home', '@work'], 'projects': ['+project_1']}
        self.assertEqual("x Text of line +project_1 @home @work",
                         self.todo.unserialize_line(line_dict))
        line_dict = {'done': False, 'line': 'Text of line 2', 'projects': ['+project_1']}
        self.assertEqual("Text of line 2 +project_1", self.todo.unserialize_line(line_dict))

    def test_unserialize(self):
        todo_list = [
            {'done': True, 'line': 'Text of line',
             'contexts': ['@home', '@work'], 'projects': ['+project_1']},
            {'done': False, 'line': 'Text of line 2', 'contexts': [], 'projects': []}
        ]
        self.todo.unserialize(todo_list)
        self.assertIn("x Text of line +project_1 @home @work\n", [line for line in self.todo])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
