from code_compiler.app.token import Tokens, Token

class Lexer:
    def __init__(self, code):
        self.code = code.strip()
        self.pos = 0
        self.tokens = []
        self.lines = self.code.split('\n')

    def tokenize(self):
        line_idx = 0
        while line_idx < len(self.lines):
            line = self.lines[line_idx].strip()
            self.pos = 0
            line_len = len(line)

            if not line:
                line_idx += 1
                continue

            while self.pos < line_len:
                char = line[self.pos]


                if char == '#':
                    break

                if char.isspace():
                    self.pos += 1
                    continue

                if char.isdigit() or (char == '-' and self.pos + 1 < line_len and line[self.pos + 1].isdigit()):
                    num = ""
                    if char == '-':
                        num += char
                        self.pos += 1
                    while self.pos < line_len and line[self.pos].isdigit():
                        num += line[self.pos]
                        self.pos += 1
                    self.tokens.append(Token(Tokens.NUMBER, int(num)))
                    continue

                if char.isalpha():
                    word = ""
                    while self.pos < line_len and (line[self.pos].isalnum() or line[self.pos] in "_"):
                        word += line[self.pos]
                        self.pos += 1
                    self.tokens.append(Token(Tokens.WORD, word))
                    continue

                if char == '_':
                    word = ""
                    word += line[self.pos]
                    self.pos += 1
                    while self.pos < line_len and (line[self.pos] not in "_"):
                        word += line[self.pos]
                        self.pos += 1
                    word += line[self.pos]
                    self.pos += 1
                    self.tokens.append(Token(Tokens.BLOCK_TYPE, word))
                    continue
                # Специальные символы
                if char in "[]+-!@":
                    self.tokens.append(Token(Tokens.WORD, char))
                    self.pos += 1
                    continue

                if char in ":":
                    self.tokens.append(Token(Tokens.COLON, char))
                    self.pos += 1
                    continue

                if char in ";":
                    self.tokens.append(Token(Tokens.SEMICOLON, char))
                    self.pos += 1
                    continue

                raise ValueError(f"Unexpected character: {char} at position {self.pos} in line {line_idx + 1}")

            line_idx += 1

        return self.tokens