import struct

import yaml

from stack_machine.config.config import instruction_mem_path, instruction_file


def load_opcodes(yaml_file: str) -> dict:
    with open(yaml_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    # Предполагаем, что в YAML есть ключ "commands" со списком словарей
    opcodes = {}
    for cmd in data['commands']:
        opcodes[cmd['desc']] = cmd['opcode']
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
            opcode = commands[cmd]
            value = 0
            if cmd in ["push_imm", "sw_to_imm_addr"] and len(parts) > 1:
                value = int(parts[1]) & 0xFFFFFF
            instruction = (value << 8) | opcode
            instructions.append(instruction)

    with open(instruction_mem_path, 'wb') as f:
        for inst in instructions:
            f.write(struct.pack('<I', inst))


if __name__ == "__main__":
    convert_to_binary("/media/ra/_work/ra/ITMO/CSA/lab4/test/test")
