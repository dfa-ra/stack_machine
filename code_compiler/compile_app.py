import os

from code_compiler.app.lexer import Lexer
from code_compiler.app.compiler import Compiler
from code_compiler.config.config import build_dir


def main(code: str):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token.tostring())
    compiler = Compiler()
    result, ep = compiler.compile(tokens)

    with open(os.path.join(build_dir, "code"), "w") as code_file:
        code_file.write(result)

    with open(os.path.join(build_dir, "start_code"), "w") as start_code_file:
        start_code_file.write(str(ep))


if __name__ == '__main__':

    path = "../test/test.forth"
    wd = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(wd, path)) as code_file:
        code = code_file.read()

    main(code)
