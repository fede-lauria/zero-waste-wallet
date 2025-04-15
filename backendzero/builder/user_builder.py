
from model_bakery import baker

from core.models import User


class UserBuilder:
    def __init__(self):
        pass

    def build(self):
        user = baker.make(User)
        return user