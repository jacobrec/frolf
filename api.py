import re
import tornado.web
import json

ACCEPTED = 'ok'

class PocketTornado():
    def __init__(self, port):
        self.port = port
        self.funcs = {}


    def listen(self):
        app = self.createApp()
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()



    def apifunction(self, path, verb):
        path = re.sub("<int>", "(\\d+)", path)
        path = re.sub("<string>", "([^\\/]+)", path)

        def holder(func):
            if path not in self.funcs:
                self.funcs[path] = {}
            self.funcs[path][verb] = func
            return func
        return holder


    def get(self, path):
        return self.apifunction(path, "get")


    def post(self, path):
        return self.apifunction(path, "post")


    def delete(self, path):
        return self.apifunction(path, "delete")


    def put(self, path):
        return self.apifunction(path, "put")


    def endpoints(self):
        handlers = []
        for path in self.funcs:
            handlers.append((path, self.handler(
                self.funcs[path]
            )))
        return handlers


    def handler(self, methods):
        class tornadoHandler(tornado.web.RequestHandler):
            def set_default_headers(self):
                self.set_header("Content-Type", "application/json")
                self.set_header("Access-Control-Allow-Origin", "*")
                self.set_header(
                    'Access-Control-Allow-Methods',
                    ', '.join([s.upper() for s in methods])
                )
        for method in methods:
            setattr(tornadoHandler, method, self.newwrapper(methods[method], method))
        return tornadoHandler


    def newwrapper(self, func, verb):
        def wrapper(self, *args):
            try:
                if verb in ("post", "put"):
                    output = func(
                        json.loads(self.request.body.decode("utf-8")),
                        *args
                    )
                elif verb in ("get", "delete"):
                    output = func(*args)
                print(output)
                if output == ACCEPTED:
                    self.set_header("Content-Type", "text/plain")
                    self.set_status(202)
                    self.finish("202: Accepted")
                else:
                    self.write(json.dumps(output))

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
