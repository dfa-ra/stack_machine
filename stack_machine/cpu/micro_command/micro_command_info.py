from .micro_command_signal_description import McSignalsDescriptions

mc_sigs_info: dict[str, McSignalsDescriptions] = {
    "alu": McSignalsDescriptions(
        {
            "open_a": 0,
            "open_b": 1,
            "add": 2,
            "sub": 3,
            "and": 4,
            "or": 5,
            "inc": 6,
            "mul": 7,
            "div": 8,
            "shl": 9,
            "shr": 10,
            "not": 11,
            "xor": 12,
            "if": 13,
            "-if": 14
        }, [0, 14]),
    "mem": McSignalsDescriptions(
        {
            "do_mem": 0,
            "read": 1
        }, [15, 16]),
    "cpu": McSignalsDescriptions(
        {
            "load_imm": 0,
            "push_stack": 1,
            "pop_stack": 2,
            "push_ret": 3,
            "load_T_a": 4,
            "load_T_b": 5,
            "load_S": 6,
            "fetch_pc": 7,
            "restore_pc": 8,
            "kill_cpu": 9,
            "over": 10,
            "call": 11,
            "load_PC": 12
        }, [17, 29]),
    "micro_command": McSignalsDescriptions(
        {
            "term_mc": 0
        }, [30]),
}
