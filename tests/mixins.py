class LoginMixin:
    default_password = "testpass123"

    def login_user(self, user, password=None):
        password = password or self.default_password
        logged_in = self.client.login(
            username=user.username,
            password=password,
        )
        self.assertTrue(logged_in)
        return logged_in