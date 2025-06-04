import struct
from typing import List, Dict

import yaml

from stack_machine.config.config import microcode_mem_file, op_table_file
from stack_machine.cpu.micro_command.micro_command_description import mc_sigs_info


class MicroCommand:
    microcode_mem_path: str = microcode_mem_file
    op_table_path: str = op_table_file

    @classmethod
    def load_binary_file(cls) -> List[int]:
        with open(cls.microcode_mem_path, "rb") as microcode_mem_f:
            data = microcode_mem_f.read()
        return list(struct.unpack("<" + "I" * (len(data) // 4), data))

    @classmethod
    def load_opcode_table(cls) -> Dict[int, int]:
        with open(cls.op_table_path, "r") as op_table_f:
            content = yaml.safe_load(op_table_f)
        return content["op_table"]

    @classmethod
    def decode_mc_word(cls, word: int) -> Dict[str, List[str]]:
        signals: Dict[str, List[str]] = {}
        for unit, desc in mc_sigs_info.items():
            start_bit = desc.bit_range[0]
            for name, bit_offset in desc.signals.items():
                bit_index = start_bit + bit_offset
                if (word >> bit_index) & 1:
                    if unit not in signals.keys():
                        signals[unit] = []
                    signals[unit].append(name)
        return signals

    @classmethod
    def decode_microcode(cls, op_code: int) -> list[dict[str, list[str]]]:
        op_table = cls.load_opcode_table()
        binary = cls.load_binary_file()

        if op_code not in op_table:
            raise ValueError(f"Unknown opcode: {op_code}")

        addr = op_table[op_code]
        decoded = []

        while True:
            word = binary[addr]
            decoded.append(cls.decode_mc_word(word))
            if (word >> 31) & 1:  # term_mc
                decoded.pop()
                break
            addr += 1

        return decoded
