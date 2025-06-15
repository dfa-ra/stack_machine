from code_compiler.app.compile_conf import commands
from code_compiler.app.compilers.compiler_text import CompilerText


class CompilerFunc:
    def __init__(self, compiler):
        self.compiler = compiler
        self.output_func = []
        self.compiler_text: CompilerText = CompilerText(self.compiler)
        pass

    def emit_func(self, command, operand=None):
        if command in commands:
            self.output_func.append(f"{command} {operand}" if commands[command] else command)
            self.compiler.pc += 1

    def compile(self, lines, address_space):
        func = []
        for line in lines:
            if line.startswith(':'):
                func_name = line[2:-1] + line[-1]
                self.compiler.functions[func_name] = self.compiler.pc
                continue

            line = line.strip()
            if line == ';':
                self.compiler_text.compile(func, address_space)
                self.output_func += self.compiler_text.output_text
                self.emit_func('ret')
                self.compiler_text.output_text = []
                func = []
                continue

            func.append(line)
