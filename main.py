from stack_machine.load_stack_machine import init_cpu, compile_code, compile_mc

if __name__ == "__main__":
    compile_mc()
    compile_code("test/test")
    cpu_ = init_cpu()
    while cpu_.running:
        cpu_.tick()
