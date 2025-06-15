import struct
from typing import Tuple

import yaml

from stack_machine.config.config import instruction_mem_path, instruction_file, data_mem_path
from stack_machine.utils.bitwise_utils import ltbe, btle


def load_opcodes(yaml_file: str) -> dict:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        raise ValueError(f"Failed to load opcodes from {yaml_file}: {e}")
    opcodes = {}
    for cmd in data['commands']:
        opcodes[cmd['desc']] = [cmd['opcode'], cmd['operand']]
    return opcodes


def convert_to_binary(input_file: str, memory_size: int) -> int | None:
    commands = load_opcodes(instruction_file)
    instructions = []
    data_entries = []
    addr_set = set()
    proc_addresses = {}  # Словарь для адресов процедур (+, -)

    current_section = None
    start_address = None
    instruction_offset = 0

    with open(input_file, 'r') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('\\'):
                continue

            parts = line.split(';')[0].split()
            if not parts:
                continue

            if parts[0] == '.data':
                current_section = 'data'
                continue
            elif parts[0] == '.text':
                current_section = 'text'
                continue

            if current_section == 'data':
                if len(parts) < 3 or parts[0] != 'var':
                    raise ValueError(
                        f"Line {line_number}: Invalid .data format, expected 'VAR <addr> BYTE <value>...' or 'VAR <addr> WORD <value>'")
                try:
                    addr = int(parts[1], 0)
                    data_type = parts[2]
                    if data_type not in ('byte', 'word'):
                        raise ValueError(f"Line {line_number}: Invalid data type, expected 'BYTE' or 'WORD'")

                    if data_type == 'word':
                        if len(parts) < 4:
                            raise ValueError(f"Line {line_number}: VAR WORD expects exactly one value")
                        values = []
                        for val in parts[3:]:
                            v = int(val, 0)
                            v = v & 0xFFFFFFFF
                            if v < 0 or v > 0xFFFFFFFF:
                                raise ValueError(f"Line {line_number}: WORD value out of range (0 to 0xFFFFFFFF)")
                            values.append(v)
                        for i in range(addr, addr + len(values) * 4):
                            if i in addr_set:
                                raise ValueError(
                                    f"Line {line_number}: Address {i} overlaps with previously defined data")
                            addr_set.add(i)
                        data_entries.append((addr, 'word', values))

                    elif data_type == 'byte':
                        if len(parts) < 4:
                            raise ValueError(f"Line {line_number}: VAR BYTE expects at least one value")
                        values = []
                        for val in parts[3:]:
                            v = int(val, 0)
                            if v < 0 or v > 255:
                                raise ValueError(f"Line {line_number}: BYTE value out of range (0 to 255)")
                            values.append(v)
                        for i in range(addr, addr + len(values)):
                            if i in addr_set:
                                raise ValueError(
                                    f"Line {line_number}: Address {i} overlaps with previously defined data")
                            addr_set.add(i)
                        data_entries.append((addr, 'byte', values))

                except ValueError as e:
                    if str(e).startswith("Line"):
                        raise
                    raise ValueError(f"Line {line_number}: Invalid address or value in .data")

            elif current_section == 'text':
                if parts[0] == '_start':
                    if start_address is not None:
                        raise ValueError(f"Line {line_number}: Multiple _start directives found")
                    start_address = instruction_offset
                    continue

                cmd = parts[0]
                opcode, has_arg = commands[cmd]

                if has_arg:
                    if len(parts) < 2:
                        raise ValueError(f"Line {line_number}: Command '{cmd}' requires an argument")
                    if len(parts) > 2:
                        raise ValueError(f"Line {line_number}: Too many arguments for command '{cmd}'")
                    try:
                        value = int(parts[1], 0)
                        value &= 0xFFFFFFFF
                    except ValueError:
                        raise ValueError(f"Line {line_number}: Invalid argument for command '{cmd}': {parts[1]}")
                    instructions.append((opcode, value))
                    instruction_offset += 5
                else:
                    instructions.append((opcode, None))
                    instruction_offset += 1

            else:
                raise ValueError(f"Line {line_number}: No section defined (.data, .text, or .proc)")

    with open(instruction_mem_path, 'wb') as f:
        for opcode, value in instructions:
            f.write(struct.pack('B', opcode))
            if value is not None:
                f.write(struct.pack('<I', value))

    if data_entries:
        with open(data_mem_path, 'wb') as f:
            max_addr = 0
            for addr, data_type, values in data_entries:
                if data_type == 'word':
                    max_addr = max(max_addr, addr + len(values) * 4)
                elif data_type == 'byte':
                    max_addr = max(max_addr, addr + len(values))
            if max_addr > memory_size:
                raise ValueError("Data memory size exceeds")
            data_memory = bytearray(memory_size)
            for addr, data_type, values in data_entries:
                if addr < 0 or addr + (4 if data_type == 'word' else len(values)) > len(data_memory):
                    raise ValueError(f"Invalid data memory address: {addr}")
                if data_type == 'word':
                    for i, value in enumerate(values):
                        struct.pack_into('<I', data_memory, addr + i*4, value)
                else:
                    for i, value in enumerate(values):
                        data_memory[addr + i] = value

            f.write(data_memory)

    return start_address


def get_decompiled_code(num_line: int = 0):
    with open(instruction_file, 'r') as f:
        data = yaml.safe_load(f)["commands"]
        opcode_to_mnemonic = {cmd["opcode"]: cmd["desc"] for cmd in data}
        opcode_has_arg = {cmd["opcode"]: cmd.get("operand", False) for cmd in data}

    with open(instruction_mem_path, 'rb') as f:
        byte_data = f.read()

    result = []
    count = 0
    index = 0

    while index < len(byte_data):
        opcode = byte_data[index]
        index += 1

        mnemonic = opcode_to_mnemonic.get(opcode, f"UNKNOWN_{hex(opcode)}")
        has_arg = opcode_has_arg.get(opcode, False)

        if has_arg:
            if index + 4 > len(byte_data):
                result.append(f"  ERROR: Incomplete argument for {mnemonic} at byte {index - 1}")
                break
            value = struct.unpack_from('<I', byte_data, index)[0]
            index += 4
            if count == num_line:
                result.append(f"  {mnemonic} 0x{value:08X}  <--")
            else:
                result.append(f"  {mnemonic} 0x{value:08X}")
        else:
            if count == num_line:
                result.append(f"  {mnemonic}  <--")
            else:
                result.append(f"  {mnemonic}")
        count += 1

    return "\n".join(result)


def get_data_meminfo(start: int = 0, end: int = 0):
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
    print(convert_to_binary("../../build/code", 30))
    print(get_decompiled_code())
    print(get_data_meminfo())
