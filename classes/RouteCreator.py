class RouteCreator:

    def __init__(self):
        self.__routes = None

    def set_path(self, path):
        self.__path = path
        return self


    def create(self):
        routes = self.__path.split('/')
        del routes[0]
        self.__routes = routes
        return self

    def get_routes(self):
        return self.__routes
