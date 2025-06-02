from stack_machine.cpu.micro_command.micro_command_info import mc_sigs_info
from stack_machine.utils.bitwise_utils import set_int_cut, get_int_cut


class MicroCommand:
    def __init__(self, signals: list[tuple[str, list[str]]], desc: str = ""):
        self.bits: int = 0
        self.desc = desc
        for sig in signals:
            name = sig[0]
            for signal_bit in sig[1]:
                self.bits = set_int_cut(self.bits,
                                        [mc_sigs_info[name].signals[signal_bit] + mc_sigs_info[name].sig_range[0]], 1)

    def get_signal(self, name: str) -> dict[str, bool]:
        return mc_sigs_info[name].get_signal_as_dict(get_int_cut(self.bits, mc_sigs_info[name].sig_range))
