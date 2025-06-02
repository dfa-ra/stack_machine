# просто пара удобных функций вокруг bytearray
class DataMem:
    def __init__(self, size: int, io_addr: list[int], io_data: list[int]):
        self.mem = bytearray(size)
        self.size = size
        self.input = io_addr[0]
        self.output = io_addr[1]
        self.input_stream = io_data
        self.output_stream: list[int] = []

    def write(self, address: int, value: int) -> None:
        if address <= self.size - 4:
            if address == self.output:
                self.output_stream.append(value)
            for i in range(4):
                self.mem[address + i] = (value & 0xFF)
                value >>= 8
        else:
            raise ValueError("Attempting to write memory out of address space")

    def write_byte(self, address: int, value: int) -> None:
        if address < self.size:
            if address == self.output:
                self.output_stream.append(value & 0xFF)
            self.mem[address] = (value & 0xFF)
        else:
            raise ValueError("Attempting to write memory out of address space")

    def read_byte(self, address: int) -> int:
        if address < self.size:
            if address == self.input:
                ret = self.input_stream[0]
                self.input_stream.pop(0)
                return ret & 0xFF
            return self.mem[address]
        else:
            raise ValueError("Attempting to read memory out of address space")

    def read(self, address: int) -> int:
        if address <= self.size - 4:
            if address == self.input:
                ret = self.input_stream[0]
                self.input_stream.pop(0)
                return ret
            ret = 0
            for i in range(4, 0, -1):
                ret <<= 8
                ret |= self.mem[address + i - 1]
            return ret
        else:
            raise ValueError("Attempting to read memory out of address space")
