from stack_machine.load_stack_machine import init_cpu, compile_code, compile_mc
from stack_machine.utils.console_layout import ConsoleLayout

if __name__ == "__main__":
    compile_mc()
    compile_code("test/test")


    console = ConsoleLayout()
    console.run()


    # while cpu_.running:
    #     cpu_.tick()
