
from stack_machine.cpu.signals import CommonSignal


class AluUnit:
    def __init__(self, cpu):

        self.cpu = cpu



        # по аналогии можешь добавить
        self.open_a = [0]
        self.open_b = [1]
        self.add = [2]
        self.sub = [3]
        self.and_ = [4]
        self.or_ = [5]

    def handle(self, signal):
        self.left = 0
        self.right = 0
        if "open_a" in signal:
            self.left = self.cpu.get_reg("A")
        if "open_b" in signal:
            self.right = self.cpu.get_reg("B")
        if "open_l" in signal:
            self.left = self.cpu.data_stack.pop()
        if "open_r" in signal:
            self.right = self.cpu.data_stack.pop()
        if "add" in signal:
            if "if" in signal:
                if self.cpu.data_stack.get_T() != 0:
                    return self.left
            if "-fi" in signal:
                if self.cpu.data_stack.get_T() < 0:
                    return self.left
            return self.left + self.right
        if "sub" in signal:
            return self.left - self.right
        if "and" in signal:
            return self.left & self.right
        if "or" in signal:
            return self.left | self.right
        if "inc" in signal:
            return self.left + 1
        if "mul" in signal:
            return self.left * self.right
        if "div" in signal:
            return self.left // self.right
        if "shl" in signal:
            return self.left << 1
        if "shr" in signal:
            return self.left >> 1
        if "not" in signal:
            return ~self.left
        if "xor" in signal:
            return self.left ^ self.right
        return 0

