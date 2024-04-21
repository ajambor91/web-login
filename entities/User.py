import hashlib

class User:
    def __init__(self, login, password):
        self.login = login
        self.password = self.__hash_pass(password)

    def __hash_pass(self, password):
        p_bytes = password.encode('utf-8')
        return  hashlib.sha224(p_bytes).hexdigest()