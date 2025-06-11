import os
import textwrap
import time

from stack_machine.inst_compiler.compiler import get_decompile_code, get_meminfo
from stack_machine.load_stack_machine import init_cpu


def gen_name(name: str, length: int):
    name = "┌" + "─" * (length - 2) + "┐" + "\n" + "│" + name + (length - len(name) - 2) * " " + "│\n" + "└" + "─" * (
            length - 2) + "┘" + "\n"
    return name


def render_block(text, x_start, y_start, width, height):
    # Разбиваем текст на строки и переносим длинные строки
    lines = []
    for line in text.split('\n'):
        # Используем textwrap.wrap для переноса строк
        wrapped_lines = textwrap.wrap(line, width=width, replace_whitespace=False, drop_whitespace=False)
        lines.extend(wrapped_lines if wrapped_lines else [''])  # Добавляем пустую строку, если строка пустая

    # Ограничиваем количество строк по высоте блока
    for i, line in enumerate(lines):
        if i >= height:
            break
        # Убедимся, что строка не превышает ширину блока
        padded_line = line.ljust(width)[:width]
        print(f"\033[{y_start + i + 1};{x_start + 1}H{padded_line}", end='')


def get_instruction():
    msg = ("  tick(t) - выполнять программу по тикам\n"
           "  dump_chunk(dc) - сделать дапм чанка в определённом диапазоне\n"
           "  delay - установить задержку при работе процессора\n"
           "  reinit_cpu(rc) - заново проинициализировть cpu\n"
           "  go - запустить работу\n"
           "  stop - остановить работу\n"
           "  inst_mnem(im) - Показать мнемоники инструкций\n"
           "  inst_byte(ib) - Показать бинарные инструкции\n")
    return msg


class CommandsInvoker:
    def __init__(self, console_layout):
        self.left_chunk_border = 0
        self.right_chunk_border = 0
        self.commands = {
            "t": lambda args: [
                console_layout.update_module_data(
                    3,
                    get_decompile_code(self.console_layout.cpu.get_reg("PC"))
                ),
                self.console_layout.cpu.tick(),
                console_layout.update_module_data(5, self.console_layout.cpu._print_state()),
                console_layout.update_module_data(
                    1,
                    self.console_layout.cpu.mem.get_meminfo(self.left_chunk_border, self.right_chunk_border)
                ),
            ],
            "dc": lambda args: [
                console_layout.update_module_data(
                    1,
                    self.console_layout.cpu.mem.get_meminfo(self.left_chunk_border, self.right_chunk_border)
                )
            ],
            "rc": lambda args: [
                console_layout.reinit_cpu(),
                console_layout.update_module_data(
                    3,
                    get_decompile_code(self.console_layout.cpu.get_reg("PC"))
                ),
                console_layout.update_module_data(5, self.console_layout.cpu._print_state()),
                console_layout.update_module_data(
                    1,
                    self.console_layout.cpu.mem.get_meminfo(self.left_chunk_border, self.right_chunk_border)
                ),
            ],
            "go": lambda args: [
                console_layout.cpu_run(),
                console_layout.update_module_data(
                    3,
                    get_decompile_code(self.console_layout.cpu.get_reg("PC"))
                ),
                console_layout.update_module_data(5, self.console_layout.cpu._print_state()),
                console_layout.update_module_data(
                    1,
                    self.console_layout.cpu.mem.get_meminfo(self.left_chunk_border, self.right_chunk_border)
                ),
            ],
            "stop": lambda args: setattr(self.console_layout.cpu, "stop_flag", int(args[1])),
            "im": lambda args: [
                console_layout.update_module_data(
                    3,
                    get_decompile_code(self.console_layout.cpu.get_reg("PC"))
                )
            ],
            "ib": lambda args: [
                console_layout.update_module_data(
                    3,
                    get_meminfo(self.left_chunk_border, self.right_chunk_border)
                )
            ]
        }
        self.console_layout = console_layout

    def execute(self, command, args):
        if command in self.commands.keys():
            self.commands[command](args)
            self.console_layout.render_layout()


class ConsoleLayout:
    def __init__(self, ep: int):
        self.ep = ep
        self.cpu = init_cpu(self.ep)

        self.invoker = CommandsInvoker(self)

        self.terminal_size = os.get_terminal_size()
        self.width = self.terminal_size.columns
        self.height = self.terminal_size.lines
        # Пример данных от модулей (замените на реальные функции модулей)
        self.module1_name = "ЧАНК ПАМЯТЬ"
        self.module3_name = "МНЕМОНИКИ/БАЙТЫ ИНСТРУКЦИЙ"
        self.module4_name = "КОМАНДЫ"
        self.module5_name = "ИНФОРМАЦИЯ ТИКА"
        self.module1_data = ""
        self.module3_data = ""
        self.module4_data = get_instruction()
        self.module5_data = ""
        self.size_changed = False

    def reinit_cpu(self):
        self.cpu = init_cpu(self.ep)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def cpu_run(self):
        while self.cpu.running and not self.cpu.stop_flag:
            self.cpu.tick()
            self.render_layout()

    def render_layout(self):
        self.clear_screen()

        # Блок 1: 1/3 ширины, прижат к правому краю
        block1_width = self.width // 3
        block1_x = self.width - block1_width
        block1_text = gen_name(self.module1_name, block1_width) + self.module1_data
        render_block(block1_text, block1_x, 0, block1_width, self.height // 1.1)

        # Блок 2: остаток ширины, прижат к низу (ввод команд)
        block2_width = self.width - block1_width
        block2_height = self.height // 6
        block2_y = self.height - block2_height
        block2_text = "Введите команду: "
        render_block(block2_text, 0, block2_y, block2_width, block2_height)

        # Блок 3: по центру
        block3_width = self.width // 3
        block3_x = (self.width - block3_width) // 2
        block3_text = gen_name(self.module3_name, block1_width) + self.module3_data
        render_block(block3_text, block3_x, 0, block3_width, self.height // 1.1)

        # Блок 4: слева
        block4_width = self.width // 3
        block4_height = self.height // 2
        block4_text = gen_name(self.module4_name, block1_width) + self.module4_data
        render_block(block4_text, 0, 0, block4_width, block4_height)

        # Блок 5: слева снизу
        block5_width = self.width // 3
        block5_height = self.height // 2
        block5_text = gen_name(self.module5_name, block1_width) + self.module5_data
        block5_y = self.height - block5_height - block2_height
        render_block(block5_text, 0, block5_y, block5_width, block5_height)

    def update_module_data(self, module, data):
        if module == 1:
            self.module1_data = data
        elif module == 3:
            self.module3_data = data
        elif module == 4:
            self.module4_data = data
        elif module == 5:
            self.module5_data = data

    def check_terminal_size(self):
        current_size = os.get_terminal_size()
        if current_size.columns != self.width or current_size.lines != self.height:
            self.width = current_size.columns
            self.height = current_size.lines
            self.size_changed = True
        else:
            self.size_changed = False

    def run(self):
        self.render_layout()

        while True:
            # Проверяем, изменился ли размер терминала
            self.check_terminal_size()
            if self.size_changed:
                self.render_layout()

            try:
                print(f"\033[{self.height - (self.height // 6) + 1};17H", end='', flush=True)
                command = input()
                if command.lower() == "exit":
                    print("Exiting...")
                    break
                else:
                    args = command.split(" ")

                    self.invoker.execute(command.lower(), args=args[1:])
            except KeyboardInterrupt:
                print("Exiting...")
                break

            time.sleep(0.1)
