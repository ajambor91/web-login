import functools
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler
import json
import re
from model.Response import Response
def extract_params(input_string):
    pattern = r'(\w+):([^/]+)'
    matches = re.findall(pattern, input_string)
    params_dict = {key: value for key, value in matches}
    return params_dict


def get(url, params = None, guard = None):
    def decorate(func):
        mapped_params = extract_params(params) if params is not None else None
        setattr(func, '__url__', url)
        setattr(func, '__params__', mapped_params)
        setattr(func, '__http_method__', 'GET')
        setattr(func, '__guard__', guard if guard is not None else None)


        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            return func(instance, *args, **kwargs)

        return wrapper

    return decorate


def post(url, params = None, guard = None):
    def decorate(func):
        mapped_params = extract_params(params) if params is not None else None

        setattr(func, '__url__', url)
        setattr(func, '__params__', mapped_params)
        setattr(func, '__http_method__', 'POST')
        setattr(func, '__guard__', guard if guard is not None else None)

        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            return func(instance, *args, **kwargs)

        return wrapper

    return decorate


def controller(url, guard = None):
    def decorate(cls):
        setattr(cls, '__url__', url)
        setattr(cls, '__guard__', guard if guard is not None else None)
        class NewClass(cls):
            routes = {}
            arrpath = None
            def __init__(self, server, arrpath):
                cls.__init__(self)
                self.arrpath = arrpath
                self.server = server
                self.guard = getattr(self, '__guard__')
                self.route = getattr(self, '__url__')

            def __get_methods(self):
                for key, value in cls.__dict__.items():

                    if hasattr(cls, key) and callable(getattr(cls, key)) and hasattr(getattr(cls, key), '__wrapped__'):
                        method = getattr(cls, key)
                        http_method = getattr(method, '__http_method__')
                        self.routes.update({
                            self.__get_decorators_args(method).replace('/',''): {'key': key, 'method': http_method}
                        })

            def __get_decorators_args(self, method):
                argument = method.__url__
                return argument

            def __get_path(self):
                parsed_path = urlparse(self.server.path)
                query_params = parse_qs(parsed_path.query)
                path = parsed_path.path.split('/')
                el = path[-1]
                return el
            def __guard(self):
                if self.guard is None:
                    return True
                is_exist = self.guard.guard('sjdhakujfgejhfg')
                if is_exist is False:
                    self.__send_response(Response())
                    return False
                else:
                    return True


            def __send_response(self, response: Response = Response()):
                self.server.send_response(response.get_response().get('code'))
                print('789798', response.get_response().get('headers').get_headers())
                self.server.send_header(response.get_response().get('headers').get_headers().items())
                self.server.end_headers()
                body = {
                    "message": response.get_response().get('message')
                }
                body.update({"body": response.get_response().get('message')})
                self.server.wfile.write(json.dumps(body).encode('utf-8'))
            def __send_unauthorized(self, response: Response = Response()):
                self.server.send_response(401)
                self.server.send_header('Content-type', 'application/json')
                self.server.end_headers()
                self.server.wfile.write(json.dumps({"message": "Unauthorized "}).encode('utf-8'))
            def __send_not_found(self, response: Response = Response()):
                self.server.send_response(404)
                self.server.send_header('Content-type', 'application/json')
                self.server.end_headers()
                self.server.wfile.write(json.dumps({"message": "Not Found"}).encode('utf-8'))

            def __send_ok(self, response: Response = Response()):
                self.server.send_response(200)
                self.server.send_header('Content-type', 'application/json')
                self.server.end_headers()
                self.server.wfile.write(json.dumps(response).encode('utf-8'))
            def __get_call(self):
                self.__get_methods()
                url = self.__get_path()
                to_call = self.routes.get(url)
                return to_call

            def do_GET(self):
                if self.__guard() is False:
                    return

                to_call = self.__get_call()
                if to_call is None:
                    return
                if to_call.get('method') == 'GET':
                    method = getattr(self, to_call.key)
                    response = method()
                    self.__send_ok(response)

            def do_POST(self):
                if self.__guard() is False:
                    return
                to_call = self.__get_call()
                print('tocl', to_call)
                if to_call is None:
                    return
                if to_call.get('method') == 'POST':
                    content_length = int(self.server.headers['Content-Length'])
                    post_data = self.server.rfile.read(content_length)
                    request_data = json.loads(post_data.decode('utf-8'))
                    method = getattr(self, to_call.get('key'))
                    response = method()
                    self.__send_ok(response)

        return NewClass

    return decorate
