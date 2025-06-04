class McSignalsDescriptions:
    def __init__(self, signals: dict[str, int], bit_range: list[int]):
        self.signals = signals
        self.bit_range = bit_range


mc_sigs_info: dict[str, McSignalsDescriptions] = {
    "alu": McSignalsDescriptions(
        {
            "open_a": 0, "open_b": 1, "open_l": 2, "open_r": 3, "add": 4,
            "sub": 5, "and": 6, "or": 7,
            "inc": 8, "mul": 9, "div": 10, "shl": 11, "shr": 12, "not": 13,
            "xor": 14, "if": 15, "-if": 16
        }, [0, 16]),
    "mem": McSignalsDescriptions(
        {"write": 0, "read": 1}, [17, 18]),
    "cpu": McSignalsDescriptions(
        {
            "load_imm": 0, "push_stack": 1, "pop_stack": 2, "push_ret": 3,
            "load_T_a": 4, "load_T_b": 5, "fetch_pc": 6,
            "restore_pc": 7, "kill_cpu": 8, "over": 9, "call": 10,
            "load_PC": 11
        }, [19, 30]),
    "micro_command": McSignalsDescriptions({"term_mc": 0}, [31])
}
