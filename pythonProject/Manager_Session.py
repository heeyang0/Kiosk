# manager.py

class Manager:
    logged_in_user_id = None

    @classmethod
    def login(cls, user_id):
        cls.logged_in_user_id = user_id

    @classmethod
    def is_logged_in(cls):
        return cls.logged_in_user_id is not None

    @classmethod
    def logout(cls):
        cls.logged_in_user_id = None

    @classmethod
    def get_logged_in_user_id(cls):
        return cls.logged_in_user_id
