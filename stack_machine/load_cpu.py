from stack_machine.cpu import Cpu
from stack_machine.cpu.instruction import Instruction
from stack_machine.cpu.mem import InstructionMem, DataMem
from stack_machine.cpu.micro_command import MicroCommand


# mc_sigs_info : dict[str, mc_signals_descriptions] = {
#     "alu": mc_signals_descriptions( {"open_a": 0,"open_b": 1,"add": 2,"sub": 3,"and": 4,"or": 5,}),
#     "mem": mc_signals_descriptions( {"do_mem": 0,"write_read": 1}),
#     "cpu": mc_signals_descriptions( {"load_imm": 0,"push_stack": 1,"pop_stack": 2,"push_ret": 3,"load_T": 4,"load_S": 5,
#                               "fetch_pc": 6,"restore_pc": 7,"kill_cpu": 8,}),
#     "micro_command": mc_signals_descriptions( {"term_mc": 0}),
# }

def load_cpu() -> Cpu:
    mc_: list[MicroCommand] = [ # manually setting up microcommands, u can make beautiful constructor for micro_command class and it'll be readable
        # fst block
        MicroCommand([("alu", ["open_b", "add"]), ("cpu", ["load_imm", "push_stack"])], "push_imm"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"]), ("cpu", ["load_imm"])], "lw_from_im_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "add"]),  ("mem", ["do_mem", "read"])], "lw_from_a_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr_inc_a"),
        MicroCommand([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["load_imm", "pop_stack"])], "sw_to_imm_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_b_addr"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr_inc_a"),
        MicroCommand([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "load_T_a_pop"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_b", "pop_stack"])], "load_T_b_push"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "add"]), ("cpu", ["push_stack"])], "push_a"),
        MicroCommand([("micro_command", ["term_mc"])]),
        # arithm
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "+"),
        MicroCommand([("cpu", ["load_T_b", "pop_stack"])]),
        MicroCommand([("alu", ["open_a", "open_b", "add"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "-"),
        MicroCommand([("cpu", ["load_T_b", "pop_stack"])]),
        MicroCommand([("alu", ["open_a", "open_b", "sub"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "*"),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])]),
        MicroCommand([("alu", ["open_b", "open_b", "mul"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "/"),
        MicroCommand([("cpu", ["load_T_b", "pop_stack"])]),
        MicroCommand([("alu", ["open_a", "open_b", "div"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "<<"),
        MicroCommand([("alu", ["open_a", "shl"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], ">>"),
        MicroCommand([("alu", ["open_a", "shr"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "not"),
        MicroCommand([("alu", ["open_a", "not"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["load_T_a", "pop_stack"])], "xor"),
        MicroCommand([("cpu", ["load_T_b", "pop_stack"])]),
        MicroCommand([("alu", ["open_a", "open_b", "xor"]), ("cpu", ["push_stack"])]),
        MicroCommand([("micro_command", ["term_mc"])]),
        # thd block
        MicroCommand([("alu", ["open_a", "add"]), ("cpu", ["load_T_a", "push_stack"])], "dup"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["pop_stack"])], "pop"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["over"])], "over"),
        MicroCommand([("micro_command", ["term_mc"])]),
        # control flow insts
        MicroCommand([("alu", ["open_a", "open_b", "add"]), ("cpu", ["load_PC", "load_imm", "fetch_pc"])], "jmp"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "open_b", "add"]), ("cpu", ["load_PC", "load_imm", "call"])], "call"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["restore_pc"])], "ret"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("alu", ["open_a", "open_b", "add", "if"]), ("cpu", ["load_PC", "load_imm", "fetch_pc"])], "if"),
        MicroCommand([("micro_command", ["term_mc"])]),
        MicroCommand([("cpu", ["kill_cpu"])], "halt"),
        MicroCommand([("micro_command", ["term_mc"])]),
    ]
    insts = [ # manually setting up instructions
        # imm                      mc_addr
        Instruction.generate_inst(mc_, "push_imm", 74),
        Instruction.generate_inst(mc_, "if", -1),
        Instruction.generate_inst(mc_, "halt", -1),
    ]
    # 0b0_0000000_00_000000
    i_mem = InstructionMem(insts)
    mem = DataMem(32, [80, 84], [1, 2, 3, 4, 5])
    return Cpu(8, mem, i_mem, mc_, 0)