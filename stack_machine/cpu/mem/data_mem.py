import os

from stack_machine.config.config import data_mem_path


def initialize_memory_file(file_path: str, size_bytes: int):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(b'\x00' * size_bytes)


class DataMem:
    def __init__(self, size: int, io_addr: list[int], io_data: list[int]):
        initialize_memory_file(data_mem_path, size)
        self.data_mem_path = data_mem_path
        # Читаем бинарный файл
        with open(data_mem_path, 'rb') as f:
            byte_data = f.read()
            if len(byte_data) % 4 != 0:
                raise ValueError("Binary file size must be a multiple of 4 bytes")
            self.size = len(byte_data)  # Размер в байтах
            self.mem = bytearray(byte_data)  # Загружаем данные в bytearray для работы
        self.input = io_addr[0]
        self.output = io_addr[1]
        self.input_stream = io_data
        self.output_stream: list[int] = []

    def _sync_to_file(self):
        # Сохраняем изменения в бинарный файл
        with open(self.data_mem_path, 'wb') as f:
            f.write(self.mem)

    def write(self, address: int, value: int) -> None:
        if address <= self.size - 4:
            if address == self.output:
                self.output_stream.append(value)
            # Записываем 32-битное слово в little-endian
            for i in range(4):
                self.mem[address + i] = (value & 0xFF)
                value >>= 8
            self._sync_to_file()  # Сохраняем изменения в файл
        else:
            raise ValueError("Attempting to write memory out of address space")

    def write_byte(self, address: int, value: int) -> None:
        if address < self.size:
            if address == self.output:
                self.output_stream.append(value & 0xFF)
            self.mem[address] = (value & 0xFF)
            self._sync_to_file()  # Сохраняем изменения в файл
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
            # Читаем 32-битное слово в little-endian
            ret = 0
            for i in range(4, 0, -1):
                ret <<= 8
                ret |= self.mem[address + i - 1]
            return ret
        else:
            raise ValueError("Attempting to read memory out of address space")