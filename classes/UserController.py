from functions.rest_api import controller, get, post
from repos.UserRepo import UserRepo
from entities.User import User
@controller('/user')
class UserController:

    def __init__(self):

        self.repo = UserRepo()

    @post('/insert')
    def test(self):
        self.repo = UserRepo()
        # self.repo.insert_user(User(login='test', data='data'))
        return {
                'message': 'insert',
                'method': 'POST',
            }
