from dataclasses import dataclass
from typing import Dict, Callable

from stack_machine.cpu.mem import DataMem, InstructionMem
from stack_machine.cpu.micro_command import MicroCommand
from stack_machine.cpu.stack import Stack
from stack_machine.cpu.units import DecoderUnit, MemUnit, AluUnit


@dataclass
class SignalHandler:
    name: str
    action: Callable[['Cpu', int], None]

class Cpu:
    def __init__(
            self,
            stack_size: int,
            mem: DataMem,
            i_mem: InstructionMem,
            mc_mem: list[MicroCommand],
            ep: int
    ):
        self.data_stack: Stack = Stack(stack_size)
        self.ret_stack: Stack = Stack(stack_size)
        self.mem: DataMem = mem
        self.i_mem: InstructionMem = i_mem
        self.regs = [0 for _ in range(4)]
        self.reg_names = {"A": 0, "B": 1, "PC": 2, "I": 3}
        self.set_reg("PC", ep)
        self.alu: AluUnit = AluUnit(self)
        self.mem_unit: MemUnit = MemUnit(self)
        self.decoder: DecoderUnit = DecoderUnit(self)
        self.last_alu_output = 0
        self.mc_mem = mc_mem
        self.tick_count = 0
        self.running = True

        # Определяем обработчики сигналов
        self.loads_signals_handlers: Dict[str, SignalHandler] = {
            "load_imm": SignalHandler("load_imm", lambda cpu, imm: cpu.set_reg("B", imm)),
            "load_T_a": SignalHandler("load_T_a", lambda cpu, _: cpu.set_reg("A", cpu.data_stack.get_T())),
            "load_T_b": SignalHandler("load_T_b", lambda cpu, _: cpu.set_reg("B", cpu.data_stack.get_T())),
            "load_S": SignalHandler("load_S", lambda cpu, _: cpu.set_reg("B", cpu.data_stack.get_S())),
            "load_PC": SignalHandler("load_PC", lambda cpu, _: cpu.set_reg("A", cpu.get_reg("PC"))),
        }

        self.signals_handlers: Dict[str, SignalHandler] = {
            "fetch_pc": SignalHandler("fetch_pc", lambda cpu, _: cpu.set_reg("PC", cpu.last_alu_output)),
            "push_stack": SignalHandler("push_stack", lambda cpu, _: cpu.data_stack.push(cpu.last_alu_output)),
            "pop_stack": SignalHandler("pop_stack", lambda cpu, _: cpu.data_stack.pop()),
            "call": SignalHandler("call", lambda cpu, _: [cpu.ret_stack.push(cpu.get_reg("PC")),
                                                          cpu.set_reg("PC", cpu.last_alu_output)]),
            "restore_pc": SignalHandler("restore_pc",
                                        lambda cpu, _: [cpu.set_reg("PC", cpu.ret_stack.get_T()), cpu.ret_stack.pop()]),
            "over": SignalHandler("over", lambda cpu, _: cpu.data_stack.over()),
            "kill_cpu": SignalHandler("kill_cpu", lambda cpu, _: setattr(cpu, "running", False)),
        }

    def tick(self):
        pc = self.get_reg("PC")
        if pc < 0 or pc >= len(self.i_mem.inst):
            print(f"Error: PC ({pc}) out of bounds, memory size: {len(self.i_mem.inst)}")
            self.running = False
            return
        imm, tick_signals = self.decoder.handle()
        for signal in tick_signals:
            self.tick_count += 1
            cpu_signals = signal[2].val
            for sig_name in cpu_signals:
                handler = self.loads_signals_handlers.get(sig_name)
                if handler:
                    handler.action(self, imm)
            self.last_alu_output = self.alu.handle(signal[0])
            self.mem_unit.handle(signal[1])
            for sig_name in cpu_signals:
                handler = self.signals_handlers.get(sig_name)
                if handler:
                    handler.action(self, imm)
        self._print_state()

    def _print_state(self):
        cpu_condition = f"""tick {self.tick_count}
A  {self.regs[0]}
B  {self.regs[1]}
PC {self.regs[2]}
I  {self.regs[3]}
MEM {self.mem.mem}
data_stack {self.data_stack.stack}"""
        print(cpu_condition)
        print()

    def get_reg(self, reg: int | str) -> int:
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        return self.regs[reg]

    def set_reg(self, reg: int | str, val: int) -> None:
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        self.regs[reg] = val