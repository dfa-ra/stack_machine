# как т data_mem просто проверка на выход за границы
from stack_machine.config.config import instruction_mem_path


class InstructionMem:
    def __init__(self):
        with open(instruction_mem_path, 'rb') as f:
            byte_data = f.read()
            if len(byte_data) % 4 != 0:
                raise ValueError("Binary file size must be a multiple of 4 bytes")
            self.inst = []
            for i in range(0, len(byte_data), 4):
                word = int.from_bytes(byte_data[i:i+4], byteorder='little', signed=False)
                self.inst.append(word)

    def get_inst(self, addr: int):
        if addr >= len(self.inst):
            raise ValueError("Trying to access instruction out of bounds")
        return self.inst[addr]


