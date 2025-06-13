import yaml
import struct

from stack_machine.config.config import instruction_file, instruction_mem_path
from stack_machine.utils.bitwise_utils import btle, ltbe, tsfb


class InstructionMem:
    def __init__(self):
        with open(instruction_file, 'r') as f:
            data = yaml.safe_load(f)["commands"]
            self.opcode_has_arg = {cmd["opcode"]: cmd.get("operand", False) for cmd in data}

        with open(instruction_mem_path, 'rb') as f:
            byte_data = f.read()

        self.inst = []
        index = 0

        while index < len(byte_data):
            if index >= len(byte_data):
                raise ValueError(f"Incomplete instruction at byte {index}")
            opcode = byte_data[index]
            index += 1

            has_arg = self.opcode_has_arg.get(opcode, False)

            if has_arg:
                if index + 4 > len(byte_data):
                    raise ValueError(f"Incomplete argument for opcode {hex(opcode)} at byte {index - 1}")
                value = struct.unpack_from('<I', byte_data, index)[0]
                value = tsfb(value)
                index += 4
                self.inst.append((opcode, value))
            else:
                self.inst.append((opcode, None))

    def get_inst(self, addr: int) -> tuple:
        if addr < 0 or addr >= len(self.inst):
            raise ValueError(f"Trying to access instruction out of bounds: {addr}")
        return self.inst[addr]
