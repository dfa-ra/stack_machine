from stack_machine.cpu.instruction import Instruction
from stack_machine.cpu.signals import CommonSignal
from stack_machine.utils.bitwise_utils import cast_immediate, get_int_cut


# в тупую интерпритирует сигналы


# смотри на аддрес мк (в самой инструкции) и набивает список сигналов
class DecoderUnit:

    def __init__(self, cpu):
        self.cpu = cpu

    def handle(self) -> [int, list[list[CommonSignal]]]:
        inst_addr = self.cpu.get_reg("PC")
        inst_ = Instruction(self.cpu.i_mem.get_inst(inst_addr))
        imm = cast_immediate(get_int_cut(inst_.bits, inst_.imm), inst_.imm)
        mc_addr = get_int_cut(inst_.bits, inst_.mc_addr)
        # тут если хочешь, можешь добавить более сложную логику fetcha, но в формате инструкции заложено 255 мк, а этого хватит
        current_mc = self.cpu.mc_mem[mc_addr]
        ret_sig = []
        while not "term_mc" in current_mc.get_signal("micro_command"):
            ret_sig.append([CommonSignal(current_mc.get_signal("alu")),
                            CommonSignal(current_mc.get_signal("mem")),
                            CommonSignal(current_mc.get_signal("cpu")),
                            ])
            mc_addr += 1
            current_mc = self.cpu.mc_mem[mc_addr]
        self.cpu.set_reg("PC", inst_addr + 1)
        return imm, ret_sig
