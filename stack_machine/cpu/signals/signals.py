# просто обертка, ее можно убрать (пока делал, думал, что понадобится доп функционал)
class CommonSignal:
    def __init__(self, sig: dict[str, bool]):
        self.val = sig