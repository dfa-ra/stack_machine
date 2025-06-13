import os

from stack_machine.load_stack_machine import init_cpu, compile_code, compile_mc
from stack_machine.utils.console_layout import ConsoleLayout

if __name__ == "__main__":
    compile_mc()
    start_code = compile_code("build/code")

    console = ConsoleLayout(start_code)
    console.run()
