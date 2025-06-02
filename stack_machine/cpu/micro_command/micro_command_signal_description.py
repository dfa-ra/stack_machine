from stack_machine.utils.bitwise_utils import get_int_cut


class McSignalsDescriptions:
    def __init__(self, signals: dict[str, int], rang: list[int]):
        self.sig_range = rang
        self.signals = signals

    def get_signal_as_dict(self, signal: int) -> dict[str, bool]:
        ret = {}
        for i in self.signals.items():
            val = get_int_cut(signal, [i[1]])
            if val != 0:
                ret[i[0]] = True
        return ret
