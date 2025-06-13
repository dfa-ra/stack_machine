from stack_machine.config.config import instruction_file
from stack_machine.utils.bitwise_utils import set_int_cut
import yaml

mc_addr = [0, 7]
imm = [8, 31]


def load_opcode_map_from_yaml(filepath: str) -> dict[str, int]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    opcode_map = {}
    for command in data.get("commands", []):
        desc = command.get("desc")
        opcode = command.get("opcode")
        if desc is not None and opcode is not None:
            opcode_map[desc] = opcode
    return opcode_map


class Instruction:
    def __init__(self, val: tuple[int, int]):
        self.mc_addr = val[0]
        self.imm = val[1] if val[1] is not None else 0
        self.bits = (val[0] << 8) | self.imm

    inst = load_opcode_map_from_yaml(instruction_file)

    @classmethod
    def generate_inst(cls, op_name: str, imm_val: int) -> int:
        bits = 0
        for inst_name in cls.inst.keys():
            if inst_name == op_name:
                bits = set_int_cut(0, mc_addr, cls.inst[inst_name])
                break
        return set_int_cut(bits, imm, imm_val)
