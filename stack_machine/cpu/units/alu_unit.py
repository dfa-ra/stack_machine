
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

    def handle(self, sig: CommonSignal):
        signals = sig.val
        a = 0
        b = 0
        if "open_a" in signals:
            a = self.cpu.get_reg("A")
        if "open_b" in signals:
            b = self.cpu.get_reg("B")
        if "add" in signals:
            if "if" in signals:
                if self.cpu.data_stack.get_T() != 0:
                    return a
            if "-fi" in signals:
                if self.cpu.data_stack.get_T() < 0:
                    return a
            return a + b
        if "sub" in signals:
            return a - b
        if "and" in signals:
            return a & b
        if "or" in signals:
            return a | b
        if "inc" in signals:
            return a + 1
        if "mul" in signals:
            return a * b
        if "div" in signals:
            return a // b
        if "shl" in signals:
            return a << 1
        if "shr" in signals:
            return a >> 1
        if "not" in signals:
            return ~a
        if "xor" in signals:
            return a ^ b
        return 0

