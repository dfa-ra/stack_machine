import os

from code_compiler.app import Compiler
from code_compiler.config.config import build_dir


def main(code: str):

    compiler = Compiler()
    compiler.compile(code)
    result = compiler.get_compiled_code()
    with open(os.path.join(build_dir, "code"), "w") as code_file:
        code_file.write(result)



if __name__ == '__main__':

    path = "../test/test.forth"
    wd = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(wd, path)) as code_file:
        code = code_file.read()

    main(code)
