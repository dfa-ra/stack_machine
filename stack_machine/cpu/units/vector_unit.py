class VectorUnit:
    def __init__(self, cpu):
        self.cpu = cpu

    def slice(self):
        vec = self.cpu.vector_stack.pop()
        return vec[0], vec[1], vec[2], vec[3]
