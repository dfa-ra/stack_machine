from typing import List


class Scope:
    def __init__(self):
        self.scopes: List[List] = [[]]

    def pop(self):
        self.scopes.pop()

    def get_scope(self):
        scope = self.scopes[-1]
        self.scopes.pop()
        return scope

    def add_scope(self, scope):
        self.scopes.append(scope)

    def add_text(self, token):
        self.scopes[-1].append(token)
