from http.server import BaseHTTPRequestHandler
from pythonProject.model.Route import Route
from pythonProject.classes.PageController import PageController
from pythonProject.classes.RouteCreator import RouteCreator
from pythonProject.classes.UserController import UserController

routing_table = [Route('user', UserController)]

class Router(BaseHTTPRequestHandler):
    def __init__(self,request, client_address, server):
        super().__init__(request,client_address, server)
        self.__current_http_method = None

    def do_POST(self):
        self.__current_http_method = 'POST'
        self.__set_pathx()
        self.__route()

    def do_GET(self):
        self.__current_http_method = 'GET'
        self.__set_pathx()
        self.__route()
    def __set_pathx(self):
        self.__route_creator = RouteCreator()
        self.__routes = self.__route_creator.set_path(self.path).create().get_routes()

    def __route(self):
        root = self.__routes[0]
        for route in routing_table:
            if route.get_root() == root:
                route.set_fullpath(self.path).set_http_method(self.__current_http_method).create_controller(self).run()
                break
        PageController(self, arrpath= self.__routes).do_GET()