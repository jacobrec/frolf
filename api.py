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

                print("Success: {0} {1} ({2}) {3:.2f}ms".format(verb.upper(), self.request.path, self.request.remote_ip, ((time.time()-now)*1000)))
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


class Error404(Exception):
    pass


class Error400(Exception):
    pass
