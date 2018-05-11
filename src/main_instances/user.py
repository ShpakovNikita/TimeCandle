class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """
    def __init__(self,
                 uid_,
                 login_,
                 password_,
                 time_zone_,
                 nickname_,
                 about_):
        self.own_tasks = []
        self.projects = []
        self.uid = uid_
        self.login = login_
        self.nickname = nickname_
        self.password = password_
        self.time_zone = time_zone_
        self.about = about_
