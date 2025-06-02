from stack_machine.cpu.micro_command import MicroCommand
from stack_machine.utils.bitwise_utils import set_int_cut

mc_addr = [0, 7]
imm = [8, 31]


class Instruction:
    def __init__(self, val: int):
        self.mc_addr = mc_addr
        self.imm = imm
        self.bits = val

    @staticmethod
    def generate_inst(mcmds: list[MicroCommand], op_name: str, imm_val: int) -> int:
        bits = 0
        for i in range(len(mcmds)):
            if mcmds[i].desc == op_name:
                bits = set_int_cut(0, mc_addr, i)
                break
        return set_int_cut(bits, imm, imm_val)
