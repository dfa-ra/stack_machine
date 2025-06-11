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


def compile_code(input_file: str) -> bool:
    logger.info("Start code сopilation.")
    try:
        convert_to_binary(input_file)
        logger.info("Successfully compiled code to binary.")
        return True
    except Exception as e:
        logger.error("Compiled code to binary failed.")
        return False


def init_cpu(ep: int) -> Cpu:
    logger.info("Init cpu.")
    i_mem = InstructionMem()
    mem = DataMem(10, [80, 84], [1, 2, 3, 4, 5])
    return Cpu(8, mem, i_mem, ep)


if __name__ == '__main__':
    _cpu = init_cpu(0)

    while _cpu.running:
        _cpu.tick()