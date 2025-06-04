from stack_machine.cpu import Cpu
from stack_machine.cpu.mem import InstructionMem, DataMem
from stack_machine.inst_compiler.compiler import convert_to_binary
from stack_machine.mc_compiler.compile import compile_micro_command


def compile_mc() -> bool:
    try:
        compile_micro_command()
        return True
    except Exception as e:
        return False

def compile_code(input_file: str) -> bool:
    try:
        convert_to_binary(input_file)
        return True
    except Exception as e:
        return False


def init_cpu() -> Cpu:
    i_mem = InstructionMem()
    mem = DataMem(32, [80, 84], [1, 2, 3, 4, 5])
    return Cpu(8, mem, i_mem, 0)
