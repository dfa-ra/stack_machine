import os

from stack_machine.load_stack_machine import init_cpu, compile_code, compile_mc
from stack_machine.utils.console_layout import ConsoleLayout

if __name__ == "__main__":
    compile_mc()
    compile_code("build/code")

    with open(os.path.join("build/start_code")) as code_file:
        start_code = int(code_file.read())

    console = ConsoleLayout(start_code)
    console.run()


    # while cpu_.running:
    #     cpu_.tick()
