from stack_machine.cpu.instruction import Instruction
from stack_machine.cpu.micro_command import MicroCommand
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

        micro_commands = MicroCommand.decode_microcode(mc_addr)

        return imm, micro_commands
