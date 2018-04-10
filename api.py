"""
A simple tornado routing package
Written by Jacob and Peter
"""

import re
import time
import tornado.web
import json

ACCEPTED = 'ok'
UNDEFINED = "undefined"


class PocketTornado():
    def __init__(self):
        self.funcs = {}

    def listen(self, port):
        app = self.createApp()
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()

    def apifunction(self, path, verb, content_type):
        path = re.sub("<int>", "(\\d+)", path)
        path = re.sub("<string>", "([^\\/]+)", path)
        
        path += "/?"

        def holder(func):
            if path not in self.funcs:
                self.funcs[path] = {}
            self.funcs[path][verb] = func
            self.funcs[path][verb].content_type = content_type
            return func
        return holder

    def get(self, path, content_type=UNDEFINED):
        return self.apifunction(path, "get", content_type)

    def post(self, path, content_type=UNDEFINED):
        return self.apifunction(path, "post", content_type)

    def delete(self, path, content_type=UNDEFINED):
        return self.apifunction(path, "delete", content_type)

    def put(self, path, content_type=UNDEFINED):
        return self.apifunction(path, "put", content_type)

    def endpoints(self):
        handlers = []
        for path in self.funcs:
            handlers.append((path, self.handler(
                self.funcs[path]
            )))
        return handlers

    def handler(superself, methods):
        class tornadoHandler(tornado.web.RequestHandler):
            def set_default_headers(self):
                self.set_header("Access-Control-Allow-Origin", "*")
                self.set_header(
                    'Access-Control-Allow-Methods',
                    ', '.join([s.upper() for s in methods])
                )
        for method in methods:
            setattr(
                tornadoHandler,
                method,
                superself.newwrapper(
                    methods[method],
                    method,
                    methods[method].content_type))
        return tornadoHandler

    def newwrapper(self, func, verb, content_type):
        def wrapper(self, *args):
            now = time.time()
            try:
                if verb in ("post", "put"):
                    output = func(
                        json.loads(self.request.body.decode("utf-8")),
                        *args
                    )
                elif verb in ("get", "delete"):
                    output = func(*args)
                if output == ACCEPTED:
                    self.set_header("Content-Type", "text/plain")
                    self.set_status(202)
                    self.finish("202: Accepted")
                elif output is None:
                    self.set_header("Content-Type", "text/plain")
                    self.set_status(204)
                    self.finish()
                else:
                    self.write(output)
                    if content_type != UNDEFINED:
                        self.set_header("Content-Type", content_type)
                prettyPrintServerMessage(
                    self._status_code,
                    verb,
                    self.request.path,
                    self.request.remote_ip,
                    ((time.time() - now) * 1000))
            except (KeyError, json.decoder.JSONDecodeError, Error400):
                self.set_header("Content-Type", "text/plain")
                self.set_status(400)
                self.finish("400: Bad Request")
            except Error404:
                self.set_header("Content-Type", "text/plain")
                self.set_status(404)
                self.finish("404: Not Found")

        return wrapper

    def createApp(self):
        return tornado.web.Application([
            *self.endpoints(),
        ])


def prettyPrintServerMessage(status, verb, path, ip, time):
    
    col = None
    if 200 <= status and status < 300:
        col = colourPrinter.green
    elif 200 <= status and status < 300:
        col = colourPrinter.yellow
    elif 200 <= status and status < 300:
        col = colourPrinter.red

    verbColours = {
        "GET" : colourPrinter.green,
        "POST": colourPrinter.blue,
        "PUT": colourPrinter.yellow,
        "DELETE": colourPrinter.red
    }

    verbColour = colourPrinter.setColour(verbColours[verb.upper()])

    if time < 1000:
        timeColour = colourPrinter.setColour(colourPrinter.green)
    elif time < 5 * 1000:
        timeColour = colourPrinter.setColour(colourPrinter.yellow)
    else:
        timeColour = colourPrinter.setColour(colourPrinter.red)
    
    
    statusColour = ""
    normal = colourPrinter.resetColour()
    if col is not None:
        statusColour = colourPrinter.setColour(colourPrinter.black, col)
    
    
    print((statusColour+"|{4}|"+normal+": "+verbColour+"{0}"+normal+" {1} ({2}) "+timeColour+"{3:.2f}ms"+normal).format(
            verb.upper(), path, ip, time, str(status)))

class colourPrinter():
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7

    @staticmethod
    def setColour(forground=white, background=black):
        return "\033[3{};4{}m".format(forground, background)
    
    @staticmethod
    def resetColour():
        return "\033[0m"

class Error404(Exception):
    pass


class Error400(Exception):
    pass
