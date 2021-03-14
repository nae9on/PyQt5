class LoginException(Exception):
    def __init__(self, username):
        super().__init__(username)
        self.username = username


class UsernameAlreadyExists(LoginException):
    pass


class PasswordTooWeak(LoginException):
    pass


class InvalidUsername(LoginException):
    pass


class InvalidPassword(LoginException):
    pass