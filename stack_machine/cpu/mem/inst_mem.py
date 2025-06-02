# как т data_mem просто проверка на выход за границы
class InstructionMem:
    def __init__(self, instructions: list[int]):
        self.inst = instructions

    def get_inst(self, addr: int):
        if addr >= len(self.inst):
            raise ValueError("trying to access instruction out of bounds")
        return self.inst[addr]