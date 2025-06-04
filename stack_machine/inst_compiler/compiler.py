import struct

import yaml

from stack_machine.config.config import instruction_mem_path, instruction_file


def load_opcodes(yaml_file: str) -> dict:
    with open(yaml_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    # Предполагаем, что в YAML есть ключ "commands" со списком словарей
    opcodes = {}
    for cmd in data['commands']:
        opcodes[cmd['desc']] = [cmd['opcode'], cmd['operand']]
    return opcodes


def convert_to_binary(input_file: str):

    commands = load_opcodes(instruction_file)

    instructions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            cmd = parts[0]
            if cmd not in commands:
                raise ValueError(f"Unknown command: {cmd}")
            opcode = commands[cmd][0]
            value = 0
            if commands[cmd][1] and len(parts) > 1:
                value = int(parts[1]) & 0xFFFFFF
            instruction = (value << 8) | opcode
            instructions.append(instruction)

    with open(instruction_mem_path, 'wb') as f:
        for inst in instructions:
            f.write(struct.pack('<I', inst))


def get_decompile_code(num_line: int = 0):
    with open(instruction_mem_path, 'rb') as f:
        byte_data = f.read()
        words = [int.from_bytes(byte_data[i:i + 4], byteorder='little') for i in range(0, len(byte_data), 4)]

    with open(instruction_file, 'r') as f:
        data = yaml.safe_load(f)["commands"]
        opcode_to_mnemonic = {hex(cmd["opcode"]): cmd["desc"] for cmd in data}

    print(opcode_to_mnemonic)
    result = []
    count = 0
    for word in words:
        opcode = word & 0xFF  # Сдвигаем вправо на 24 бита и маскируем 8 бит
        print(opcode)
        # Извлекаем значение (оставшиеся 24 бита)
        value = (word >> 8) & 0xFFFFFF  # Маскируем 24 бита

        # Преобразуем opcode в мнемонику
        mnemonic = opcode_to_mnemonic.get(hex(opcode), f"UNKNOWN_{hex(opcode)}")

        # Формируем строку команды
        if value != 0:  # Если значение не нулевое, добавляем его
            if count == num_line:
                result.append(f"  {mnemonic} 0x{value:06X}  <--")
            else:
                result.append(f"  {mnemonic} 0x{value:06X}")
        else:
            if count == num_line:
                result.append("  " + mnemonic + "  <-- ")
            else:
                result.append("  " + mnemonic)
        count += 1

    return "\n".join(result)


def get_meminfo(self, start: int = 0, end: int = 0):
    mem_info: str = ""
    with open(instruction_mem_path, 'rb') as f:
        byte_data = f.read()
        if end == 0: end = len(byte_data)
        # Вывод таблицы
        mem_info += "  Addr |  0  1  2  3 |  4  5  6  7 |  8  9 10 11 |\n"
        mem_info += "  -----|-------------|-------------|-------------|\n"

        for i in range(start, end, 12):
            # Адрес в шестнадцатеричном формате
            addr = i
            # Получаем до 12 байт для текущей строки
            chunk = byte_data[i:i + 12]
            # Форматируем байты в строку, разбивая на чанки по 4 байта
            bytes_str = []
            for j in range(12):
                if j < len(chunk):
                    bytes_str.append(f"{chunk[j]:02X}")
                else:
                    bytes_str.append("  ")  # Пробелы для недостающих байт
            # Разделяем на три чанка по 4 байта
            group1 = " ".join(bytes_str[0:4])
            group2 = " ".join(bytes_str[4:8])
            group3 = " ".join(bytes_str[8:12])
            # Выводим строку
            mem_info += f"  {addr:04X} | {group1: <10} | {group2: <10} | {group3: <10} |"
            mem_info += "\n"
    return mem_info

if __name__ == "__main__":
    convert_to_binary("../../build/code")
    print(get_decompile_code())
