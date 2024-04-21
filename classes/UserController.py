from functions.rest_api import controller, get, post
from guard.UserAuthService import UserAuthService
from guard.RouteGuard import RouteGuard
from entities.User import User
@controller('/user', guard=RouteGuard())
class UserController:

    def __init__(self):

        self.auth_service = UserAuthService()

    @post('/insert')
    def insert(self):
        self.auth_service = UserAuthService()
        user = self.auth_service.register(login='test', password='data')

        return {
                'message': 'czesc ' + user.login,
                'method': 'POST',
            }

    @post('/login')
    def test(self):
        self.auth_service = UserAuthService()
        user = self.auth_service.login(login='test', password='data', session_id='sjdhakujfgejhfg')

        return {
                'message': 'czesc ' + user.login,
                'method': 'POST',
            }