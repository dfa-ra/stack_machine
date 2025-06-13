from code_compiler.app.Symbol import Symbol
from code_compiler.app.compile_conf import forbidden_var


class CompilerData:
    def __init__(self, compiler):
        self.compiler = compiler
        self.data_address = 0

    def add_data(self, name, type, size=1, values=None):
        self.compiler.symbols[name] = Symbol(self.data_address, type, size, values)
        self.data_address += size * 4

    def compile(self, lines):
        for line in lines:
            tokens = line.split()
            if tokens[-1] in forbidden_var:
                raise Exception("Forbidden variable")
            if tokens[0].startswith('['):
                name = tokens[-1]
                values = []
                for value in tokens[1:]:
                    if value == ']':
                        break
                    values.append(value)
                self.add_data(name, 'array', len(values), values)
            elif tokens[1] == 'VAR':
                self.add_data(tokens[2], 'var', 1, [int(tokens[0])])

    def get_symbol(self, name):
        return self.compiler.symbols[name]

    def get_data_section(self):
        data = ['   .data']
        for name, symbol in self.compiler.symbols.items():
            if symbol.type == 'array':
                data.append(f"var {symbol.address} word {' '.join(map(str, symbol.values))}")
            else:
                data.append(f"var {symbol.address} word {symbol.values[0]}")
        return data