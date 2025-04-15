from typing import Dict

from django.contrib.auth.models import AnonymousUser
from graphene import Schema
from graphene.test import Client

from builder.request_builder import RequestBuilder


class GraphQLClient:

    def __init__(self, schema: Schema):
        self.schema = schema
        self.authorization_token = None
        self.cookies = [(str, str)]

    def with_cookie(self, name, value):
        self.cookies.append((name, value))
        return self

    def with_authorization_token(self, value):
        self.authorization_token = value
        return self

    def execute(self, query: str, user=None, variables: Dict = {}):
        request = RequestBuilder().with_cookies(self.cookies).with_auth(self.authorization_token).get('/')
        request.user = user or AnonymousUser()
        return Client(self.schema).execute(query, context_value=request, variables=variables)
