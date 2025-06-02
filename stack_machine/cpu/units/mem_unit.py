# если читает, кладет в A. адрес берется из imm (из инструкции) и верхушки стэка
from stack_machine.cpu.signals import CommonSignal


class MemUnit:
    def __init__(self, cpu):
        self.cpu = cpu

        self.need_mem = [0]
        self.write_read = [1]

    def handle(self, sig: CommonSignal):
        signals = sig.val
        if not "do_mem" in signals:
            return
        # тут можешь поменять что куда пишет и добавить еще какихнить функций
        if not "read" in signals:
            # eg write
            addr = self.cpu.last_alu_output
            val = self.cpu.data_stack.get_T()
            self.cpu.mem.write(addr, val)
        else:
            addr = self.cpu.last_alu_output
            val = self.cpu.mem.read(addr)
            self.cpu.data_stack.push(val)
