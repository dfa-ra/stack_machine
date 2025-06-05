class McSignalsDescriptions:
    def __init__(self, signals: dict[str, int], bit_range: list[int]):
        self.signals = signals
        self.bit_range = bit_range


mc_sigs_info: dict[str, McSignalsDescriptions] = {
    "alu": McSignalsDescriptions(
        {
            "open_a": 0, "open_b": 1, "open_l": 2, "open_r": 3, "open_r_pc": 4,
            "add": 5, "sub": 6, "and": 7, "or": 8,
            "inc": 9, "mul": 10, "div": 11, "shl": 12, "shr": 13, "not": 14,
            "if": 15, "-if": 16
        }, [0, 16]),
    "mem": McSignalsDescriptions(
        {"write": 0, "read": 1}, [17, 18]),
    "cpu": McSignalsDescriptions(
        {
            "load_imm": 0, "push_stack": 1, "pop_stack": 2, "push_ret": 3,
            "load_T_a": 4, "load_T_b": 5, "fetch_pc": 6,
            "restore_pc": 7, "kill_cpu": 8, "over": 9, "call": 10, "reserve": 11
        }, [19, 30]),
    "micro_command": McSignalsDescriptions({"term_mc": 0}, [31])
}
