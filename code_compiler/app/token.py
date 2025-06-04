from enum import Enum


class Tokens(Enum):
    NUMBER = "NUMBER"
    BLOCK_TYPE = "BLOCK_TYPE"
    STRING = "STRING"
    WORD = "WORD"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    IF = "IF"
    ELSE = "ELSE"
    THEN = "THEN"
    DO = "DO"
    LOOP = "LOOP"


class Token:
    def __init__(self, type_: Tokens, value):
        self.type = type_  # "NUMBER", "WORD", "COLON", "SEMICOLON", "IF", "THEN", "DO", "LOOP"
        self.value = value

    def tostring(self):
        return f"Token: {self.type.value}, {self.value}"
