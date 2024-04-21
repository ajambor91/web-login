from repos.UserRepo import UserRepo
from entities.User import User
from guard.UserStateManager import UserStateManager
class UserAuthService(object):
    def __init__(self):
        self.__user_state = UserStateManager()
        self.__user_repo = UserRepo()
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserAuthService, cls).__new__(cls)
        return cls.instance

    def login(self, login, password, session_id):
        poss_user = User(login, password)
        user = self.__user_repo.get_user(poss_user)
        print('skjlfhgdsajlhfgjdhlsfgjdhsgfjkdhs', user)
        self.__user_state.current_user = user
        self.__set_session_id(session_id)
        user = self.get_user()
        return user if user is not None else False

    def register(self,  login, password):
        poss_user = User(login, password)
        print('reg poss',poss_user.get_data())
        user = self.__user_repo.insert_user(poss_user)
        return user if user is not None else False

    def get_user(self):
        return self.__user_state.current_user
    def __set_session_id(self, session_id):
        user = self.__user_state.current_user
        user.set_session_id(session_id)
