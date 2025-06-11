import multiprocessing

from .alu_unit import ALU
from .vector_unit import VectorUnit


def run_search(obj: ALU, signals, a, b, index, result_queue):
    result = obj.handle(signals, a, b)
    result_queue.put((index, result))


class ControlAluUnit:
    def __init__(self, cpu):

        self.cpu = cpu
        self.alu1: ALU = ALU(cpu)
        self.alu2: ALU = ALU(cpu)
        self.alu3: ALU = ALU(cpu)
        self.alu4: ALU = ALU(cpu)

    def init_alu_list(self):
        return [self.alu1, self.alu2, self.alu3, self.alu4]

    def init_operands(self, signals):
        if self.cpu.simd_type == 1:
            left = [0, 0, 0, 0]
            right = [0, 0, 0, 0]
            if "open_l" in signals:
                left = VectorUnit.slice(self.cpu.vector_stack.pop())
            if "open_r" in signals:
                right = VectorUnit.slice(self.cpu.vector_stack.pop())
            return [(left[i], right[i]) for i in range(0, len(left))]
        else:
            left = 0
            right = 0
            if "open_a" in signals:
                left = self.cpu.get_reg("A")
            if "open_b" in signals:
                right = self.cpu.get_reg("B")
            if "open_r_pc" in signals:
                left = self.cpu.get_reg("PC")
            if "open_l" in signals:
                left = self.cpu.data_stack.pop()
            if "open_r" in signals:
                right = self.cpu.data_stack.pop()
            return [left, right]

    def handle(self, signals):
        if self.cpu.simd_type == 1:
            return self.simd_handle(signals)
        else:
            return self.scalar_handle(signals)

    def scalar_handle(self, signals):
        operands = self.init_operands(signals)
        return self.alu1.handle(signals, operands[0], operands[1])

    def simd_handle(self, signals):
        results = multiprocessing.Queue()
        processes = []
        alu_list = self.init_alu_list()
        operands = self.init_operands(signals)

        for i, (obj, (a, b)) in enumerate(zip(alu_list, operands)):
            p = multiprocessing.Process(
                target=run_search,
                args=(obj, signals, a, b, i, results),
                name=f"Alu-{i + 1}"
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        process_results = [None] * len(operands)
        while not results.empty():
            index, result = results.get()
            process_results[index] = result

        return process_results
