class Route:

    def __init__(self, name, controller_class, path = None, sec = None):
        self.controller = None
        self.__current_http_method = None
        self.name = name
        self.controller_class = controller_class
        self.path = path
        self.sec = sec

    def set_http_method(self, method):
        self.__current_http_method = method
        return self
    def create_controller(self, server):
        self.controller = self.controller_class(server = server, arrpath = self.path) if hasattr(self.controller_class, '__new__') else None
        return self
    def get_root(self):
       return self.name

    def get_controller(self):
        return self.controller

    def set_fullpath(self, path):
        self.path = path
        return self

    def run(self):
        if self.__current_http_method == 'POST':
            self.controller.do_POST()
        else:
            self.controller.do_GET()

    def get_method(self):
        method = self.controller