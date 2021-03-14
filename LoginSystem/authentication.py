from login_exceptions import UsernameAlreadyExists, PasswordTooWeak, InvalidUsername, InvalidPassword
import hashlib
import json


class User:
    def __init__(self, username, password=None):
        self.username = username
        if password is not None:
            self.encrypted_password = self._encrypt_password(password)
        self.is_logged_in = False

    def _set_encrypted_password(self, encrypted_password):
        self.encrypted_password = encrypted_password

    def _encrypt_password(self, password):
        hash_string = self.username + password
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        return self._encrypt_password(password) == self.encrypted_password


class Authenticator:
    cached_users_list_file = 'users_list.json'

    def __init__(self):
        cached_data = self._get_cached_users()
        if cached_data is not None:
            cached_users = dict()
            for username in cached_data.keys():
                user = User(username)
                user._set_encrypted_password(cached_data[username])
                cached_users[username] = user
            print(cached_users)
            self.users = cached_users
        else:
            self.users = dict()

    @staticmethod
    def _get_cached_users():
        cached_data = None
        with open(Authenticator.cached_users_list_file, 'r') as file:
            try:
                cached_data = json.load(file)
            except json.JSONDecodeError:
                print('No cached users')
        return cached_data

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooWeak(username)
        self.users[username] = User(username, password)
        self.write_to_file()

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not self.users[username].check_password(password):
            raise InvalidPassword(username)

        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False

    def write_to_file(self):
        username_password_dict = {user: self.users[user].encrypted_password for user in self.users.keys()}
        with open(Authenticator.cached_users_list_file, 'w') as file:
            json.dump(username_password_dict, file)