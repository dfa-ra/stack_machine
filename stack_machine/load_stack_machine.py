from stack_machine.cpu import Cpu
from stack_machine.cpu.mem import InstructionMem, DataMem
from stack_machine.inst_compiler.compiler import convert_to_binary
from stack_machine.mc_compiler.compile import compile_micro_command
from stack_machine.utils.log import logger


def compile_mc() -> bool:
    logger.info("Start micro commands сopilation.")
    try:
        compile_micro_command()
        logger.info("Successfully compiled Micro command.")
        return True
    except Exception as e:
        logger.error("Micro command compilation failed.")
        return False


def compile_code(input_file: str) -> int | None | bool:
    logger.info("Start code сopilation.")
    try:
        start_code = convert_to_binary(input_file, 32)
        logger.info("Successfully compiled code to binary.")
        return start_code
    except Exception as e:
        logger.error("Compiled code to binary failed.")
        return False


def init_cpu(ep: int) -> Cpu:
    logger.info("Init cpu.")
    i_mem = InstructionMem()
    mem = DataMem([80, 84], [1, 2, 3, 4, 5])
    return Cpu(8, mem, i_mem, ep)


if __name__ == '__main__':

    compile_micro_command()
    start = compile_code("../build/code")
    _cpu = init_cpu(start)

    while _cpu.running:
        _cpu.tick()
