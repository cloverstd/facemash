#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import os.path
from handlers import IndexHandler, TopHandler, SetUpHandler
import torndb
import tornado.wsgi


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/top', TopHandler),
            (r'/setup', SetUpHandler),
        ]
        settings = dict(
            autoescape=None,
            xsrf_cookies=True,
            cookie_secret="",
            login_url="/login",
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)

        self.db = torndb.Connection("localhost", "facemash", "root", "xws2931336")

class BAE(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/top', TopHandler),
            (r'/setup', SetUpHandler),
        ]
        settings = dict(
            autoescape=None,
            xsrf_cookies=True,
            cookie_secret="",
            login_url="/login",
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)

        self.db = torndb.Connection("localhost", "facemash", "root", "xws2931336")


if "SERVER_SOFTWARE" in os.environ:
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(BAE())
else:
    import tornado.ioloop
    appilication = Application()
    appilication.listen(8080)
    print "http://localhost:8080"
    tornado.ioloop.IOLoop.instance().start()
