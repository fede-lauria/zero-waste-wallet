from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory


class RequestBuilder:
    def __init__(self):
        self.cookies: [(str, str)] = []
        self.headers: [(str, str)] = []
        self.user = AnonymousUser()

    def with_user(self, user: User):
        self.user = user
        return self

    def with_auth(self, auth: str):
        self.with_header('HTTP_AUTHORIZATION', auth)
        return self

    def with_cookie(self, key: str, value: str):
        self.cookies.append((key, value))
        return self

    def with_cookies(self, cookies: [(str, str)]):
        self.cookies = cookies
        return self

    def with_header(self, key: str, value: str):
        self.headers.append((key, value))
        return self

    def get(self, path: str):
        return self._build_request(RequestFactory().get(path))

    def post(self, path: str, data=None):
        return self._build_request(RequestFactory().post(path, data=data))

    def _build_request(self, request):
        request.session = {}
        request.user = self.user
        request._dont_enforce_csrf_checks = True

        for name, value in self.cookies:
            request.COOKIES[name] = value

        for key, value in self.headers:
            request.META[key] = value

        return request
