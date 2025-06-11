# если читает, кладет в A. адрес берется из imm (из инструкции) и верхушки стэка
from stack_machine.cpu.signals import CommonSignal


class MemUnit:
    def __init__(self, cpu):
        self.cpu = cpu

        self.need_mem = [0]
        self.write_read = [1]

    def handle(self, signal):
        if self.cpu.simd_type == 1:
            if "write" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.vector_stack.pop()
                self.cpu.mem.write(addr, val[0])
                self.cpu.mem.write(addr + 1, val[1])
                self.cpu.mem.write(addr + 2, val[2])
                self.cpu.mem.write(addr + 3, val[3])

            elif "read" in signal:
                addr = self.cpu.last_alu_output
                val1 = self.cpu.mem.read(addr)
                val2 = self.cpu.mem.read(addr + 1)
                val3 = self.cpu.mem.read(addr + 2)
                val4 = self.cpu.mem.read(addr + 3)
                self.cpu.vector_stack.push([val1, val2, val3, val4])

        else:
            if "write" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.data_stack.pop()
                self.cpu.mem.write(addr, val)
            if "read" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.mem.read(addr)
                self.cpu.data_stack.push(val)
