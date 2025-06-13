from code_compiler.app.compile_conf import built_in_words, commands


class CompilerText:
    def __init__(self, compiler):
        self.compiler = compiler
        self.output_text = []

    def emit(self, command, operand=None):
        if command in commands:
            self.output_text.append(f"{command} {operand}" if commands[command] else command)
            self.compiler.pc += 1

    def compile(self, lines):
        for line in lines:
            tokens = line.split()
            for token in tokens:
                if token in self.compiler.symbols:
                    if self.compiler.symbols[token].type == 'array':
                        self.emit('v_lw_from_imm_addr', self.compiler.symbols[token].address)
                    else:
                        self.emit('lw_from_imm_addr', self.compiler.symbols[token].address)
                elif token in self.compiler.functions.keys():
                    offset = self.compiler.functions[token] - self.compiler.pc - 1
                    self.emit('call', offset)
                elif token.startswith('!'):
                    if len(token) > 1:
                        if token[1] == "+" and len(token) == 2:
                            self.emit('sw_to_a_addr_inc_a')
                        elif token[1] == "b" and len(token) == 2:
                            self.emit('sw_to_b_addr')
                        else:
                            name = token[1:]
                            if self.compiler.symbols[name].type == 'array':
                                self.emit("load_T_a_pop")
                                self.emit('sw_to_a_addr')
                            else:
                                self.emit("sw_to_imm_addr", self.compiler.symbols[name].address)
                    else:
                        self.emit('sw_to_a_addr')
                elif token.startswith('@'):
                    if len(token) > 1:
                        if token[1] == "+" and len(token) == 2:
                            self.emit('lw_from_a_addr_inc_a')
                        elif token[1] == "b" and len(token) == 2:
                            self.emit('lw_from_b_addr')
                        else:
                            name = token[1:]
                            if self.compiler.symbols[name].type == 'array':
                                self.emit("load_T_a_pop")
                                self.emit('lw_from_a_addr')
                            else:
                                self.emit("lw_from_imm_addr", self.compiler.symbols[name].address)
                    else:
                        self.emit('lw_from_a_addr')
                elif token.isdigit():
                    self.emit('push_imm', token)
                elif token in built_in_words:
                    self.emit(built_in_words[token])
                else:
                    raise Exception(f'Unknown token: {token}')
