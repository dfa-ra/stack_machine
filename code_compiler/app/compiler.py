from code_compiler.app.compile_conf import commands, built_in_words
from code_compiler.app.compilers import CompilerText, CompilerData, CompilerFunc


class Compiler:
    def __init__(self):
        self.symbols = {}
        self.functions = {}
        self.output = []
        self.pc = 0

        self.compiler_data: CompilerData = CompilerData(self)
        self.compiler_text: CompilerText = CompilerText(self)
        self.compiler_func: CompilerFunc = CompilerFunc(self)

    def compile_data(self, lines):
        self.compiler_data.compile(lines)

    def compile_func(self, lines):
        self.compiler_func.compile(lines)

    def compile_text(self, lines):
        self.compiler_text.compile(lines)

    def compile(self, code):
        lines = code.strip().split('\n')
        current_section = None
        data_lines = []
        func_lines = []
        text_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line in ['_data_', '_func_', '_text_']:
                if data_lines and current_section == '_data_':
                    self.compile_data(data_lines)
                    data_lines = []
                if func_lines and current_section == '_func_':
                    self.compile_func(func_lines)
                    func_lines = []
                current_section = line
                continue
            if current_section == '_data_':
                data_lines.append(line)
            elif current_section == '_func_':
                func_lines.append(line)
            elif current_section == '_text_':
                text_lines.append(line)

        if text_lines:
            self.compile_text(text_lines)

    def get_text_section(self):
        return ['   .text'] + self.compiler_func.output_func + ['   _start'] + self.compiler_text.output_text

    def get_compiled_code(self):
        text = '\n'.join(self.compiler_data.get_data_section())
        text += "\n"
        text += '\n'.join(self.get_text_section())
        return text
