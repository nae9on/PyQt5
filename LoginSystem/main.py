from authentication import Authenticator

if __name__ == "__main__":
    authenticator = Authenticator()
    authenticator.add_user("X", "Xpassword")
    authenticator.login("X", "Xpassword")
    print(authenticator.is_logged_in("X"))
