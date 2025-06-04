from typing import Dict

from code_compiler.app.token import Tokens


class Compiler:
    def __init__(self):
        self.output = []
        self.var_output = []
        self.func_output = []
        self.text_output = []
        self.current_token = None
        self.token_index = -1
        self.tokens = []
        self.built_in_words = {
            "+": ["+"],
            "-": ["-"],
            "dup": ["dup"],
            "drop": ["pop"],
            "!": [],  # Запись в память по адресу
            "@": [],  # Загрузить в стек из адреса
            "HERE": ["push_imm 0"],  # Упрощённая заглушка для адреса
            "VAR": [],  # Обработаем в compile_constant
            "ARRAY": [],
            "HALT": ["halt"],
            ":": [],  # Объявление пользовательских меток
            ";": [],

        }
        self.user_variable: Dict[str: [int, int]] = {}
        self.user_words = {}
        self.def_start_pos = {}
        self.next_addr = 0

    def next_token(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1
        else:
            self.current_token = None

    def compile(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.output = []
        self.def_start_pos = {}

        self.next_token()
        while self.current_token:
            self.compile_word()
        func = "\n".join(self.func_output)
        var = "\n".join(self.var_output)
        text = "\n".join(self.text_output)
        return func + "\n" + var + "\n" + text, len(self.func_output)

    def compile_word(self):
        token = self.current_token
        if token.type == Tokens.BLOCK_TYPE:
            if token.value == "_data_":
                self.compile_var_block()
            elif token.value == "_func_":
                self.compile_func_block()
            elif token.value == "_text_":
                self.compile_text_block()

    def compile_var_block(self):
        self.next_token()
        while self.current_token and self.current_token.type != Tokens.BLOCK_TYPE:
            token = self.current_token
            if token.type == Tokens.NUMBER:
                self.var_output.append(f"push_imm {token.value}")
            elif token.type == Tokens.WORD:
                if token.value in self.built_in_words:
                    self.var_output.extend(self.built_in_words[token.value])
                if token.value == "VAR":
                    self.compile_variable(self.var_output)
                if token.value == "ARRAY":
                    self.compile_array_variable(self.var_output)
            self.next_token()

    def compile_func_block(self):
        self.next_token()
        while self.current_token and self.current_token.type != Tokens.BLOCK_TYPE:
            if self.current_token.value == ":":
                self.compile_definition(self.func_output)
            self.next_token()

    def compile_text_block(self):
        self.next_token()
        while self.current_token and self.current_token.type != Tokens.BLOCK_TYPE:
            token = self.current_token
            if token.type == Tokens.NUMBER:
                self.text_output.append(f"push_imm {token.value}")
            elif token.type == Tokens.WORD:
                if token.value in self.built_in_words:
                    if token.value == "!":
                        self.compile_save_variable(self.text_output)
                    elif token.value == "@":
                        self.compile_load_from(self.text_output)
                    else:
                        self.text_output.extend(self.built_in_words[token.value])
                elif token.value in self.user_words:
                    call_pos = len(self.text_output) + len(self.var_output) + len(self.func_output)
                    def_pos = self.def_start_pos[token.value]
                    offset = def_pos - call_pos - 1
                    self.text_output.append(f"call {offset}")
                elif token.value in self.user_variable:
                    self.text_output.append(f"lw_from_im_addr {self.user_variable[token.value][0]}")
                else:
                    raise ValueError(f"Unknown word: {token.value}")
            elif token.type == Tokens.COLON:
                self.compile_definition(self.text_output)
            self.next_token()

    def compile_definition(self, output):
        self.next_token()
        if not self.current_token or self.current_token.type != Tokens.WORD:
            raise ValueError("Expected word name after :")
        word_name = self.current_token.value
        if word_name in self.built_in_words or word_name in self.user_words:
            raise ValueError(f"Redefinition of word: {word_name}")

        self.def_start_pos[word_name] = len(self.func_output)
        word_code = []
        self.next_token()

        while self.current_token and self.current_token.type != Tokens.SEMICOLON:
            token = self.current_token
            if token.type == Tokens.NUMBER:
                output.append(f"push_imm {token.value}")
            elif token.type == Tokens.WORD:
                if token.value in self.built_in_words:
                    if token.value == "!":
                        self.compile_save_variable(output)
                    elif token.value == "@":
                        self.compile_load_from(self.text_output)
                    else:
                        output.extend(self.built_in_words[token.value])
                elif token.value in self.user_variable:
                    output.append(f"lw_from_im_addr {self.user_variable[token.value][0]}")
                else:
                    raise ValueError(f"Unknown word: {token.value}")
            self.next_token()

        word_code.append("ret")
        self.user_words[word_name] = word_code
        output.extend(word_code)


    def compile_variable(self, output):
        a = 1
        self.next_token()
        if not self.current_token or self.current_token.type != Tokens.WORD:
            raise ValueError("Expected constant name after 'VAR'")
        const_name = self.current_token.value
        if const_name in self.built_in_words or const_name in self.user_variable:
            raise ValueError(f"Redefinition of word: {const_name}")

        if not output or not output[-1].startswith("push_imm"):
            raise ValueError("Expected value before 'VAR'")
        addr = self.next_addr
        self.next_addr += 1
        self.user_variable[const_name] = [addr, 1]
        output.append(f"sw_to_imm_addr {addr}")

    def compile_array_variable(self, output):
        self.next_token()
        if not self.current_token or self.current_token.type != Tokens.WORD:
            raise ValueError("Expected array name after 'ARRAY'")
        array_name = self.current_token.value
        if array_name in self.built_in_words or array_name in self.user_variable:
            raise ValueError(f"Redefinition of word: {array_name}")

        if not output or not output[-1].startswith("push_imm"):
            raise ValueError("Expected array size before 'ARRAY'")

        size = int(output[-1].split()[1])
        if size <= 0:
            raise ValueError("Array size must be positive")

        addr = self.next_addr
        self.next_addr += size  # Увеличиваем адрес на размер массива
        self.user_variable[array_name] = (addr, size)  # Сохраняем адрес и размер
        output.pop()

        load_mas = []

        for i in range(size):
            if not output[-1 - i].startswith("push_imm"):
                break
            load_mas.append(f"sw_to_imm_addr {self.next_addr - i - 1}")

        output.extend(load_mas)

    def compile_save_variable(self, output):
        self.next_token()
        if not self.current_token or self.current_token.type != Tokens.WORD:
            raise ValueError("Expected variable name after '!'")
        variable_name = self.current_token.value
        if variable_name in self.built_in_words or variable_name not in self.user_variable:
            raise ValueError(f"Redefinition of word: {variable_name}")
        addr, size = self.user_variable[variable_name]

        if size > 1:
            output.append(f"push_imm {self.user_variable[variable_name][0]}")
            output.append(f"+")
            output.append(f"load_T_a_pop")
            output.append(f"sw_to_a_addr")
        else:
            output.append(f"sw_to_imm_addr {addr}")


    def compile_load_from(self, output):
        self.next_token()
        if not self.current_token or self.current_token.type != Tokens.WORD:
            raise ValueError("Expected variable after '@'")
        variable_name = self.current_token.value
        if variable_name not in self.user_variable:
            raise ValueError(f"Unknown variable: {variable_name}")

        if self.user_variable[variable_name][1] > 1:
            output.append(f"push_imm {self.user_variable[variable_name][0]}")
            output.append(f"+")
            output.append(f"load_T_a_pop")
            output.append(f"lw_from_a_addr")
        else:
            output.append(f"load_T_a_pop")
            output.append(f"lw_from_a_addr")

