#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from tornado.web import HTTPError
from tornado.ioloop import IOLoop
from tornado.web import Application, url, RequestHandler, asynchronous
from tornado.options import define, options
from tornado.escape import json_encode
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 4

from functools import wraps

import todo_txt

define("port", default="8880", help="Worker port number")
define("config", help="Config file name", default="default_config.py")
define("todo_file", help="todo.txt file path")


def method_proxy(f):
    @wraps(f)
    def wrapper(obj, *args, **kwargs):
        if 'method' in kwargs:
            method = kwargs.pop('method')
        else:
            method = None
        if method:
            return getattr(obj, method)(*args, **kwargs)
        else:
            return f(obj, *args, **kwargs)
    return wrapper

class RequestHandlerProxy(RequestHandler):

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @method_proxy
    def get(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).get(*args, **kwargs)

    @method_proxy
    def post(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).post(*args, **kwargs)

    @method_proxy
    def delete(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).delete(*args, **kwargs)

    @method_proxy
    def put(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).put(*args, **kwargs)

    @method_proxy
    def head(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).head(*args, **kwargs)

    @method_proxy
    def options(self, *args, **kwargs):
        return super(RequestHandlerProxy, self).options(*args, **kwargs)


class MainHandler(RequestHandler):

    def get(self):
        self.render('main.html')

class TodoHandler(RequestHandler):

    def initialize(self):
        self.todo = todo_txt.TodoTxt(options.todo_file)

    def get(self):
        result = []
        for line in self.todo:
            result.append({'line': line})
        result_encoded = json_encode(result)
        self.write(result_encoded)

def make_app():
    return Application(
        [
            url(r"/", MainHandler),
            url(r"/todo/", TodoHandler),
        ],
        template_path=os.path.join('static', 'html'),
        static_path=os.path.join('static'),
        debug=True,
    )

def start_app(app):
    app.listen(options.port)
    IOLoop.current().start()

def main():
    options.parse_command_line()
    if options.config:
        options.parse_config_file(options.config)
    app = make_app()
    start_app(app)

if __name__ == '__main__':
    main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
