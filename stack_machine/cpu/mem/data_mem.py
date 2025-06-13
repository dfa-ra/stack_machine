import os

from stack_machine.config.config import data_mem_path
from stack_machine.utils.bitwise_utils import btle, ltbe, tsfb


class DataMem:
    def __init__(self, io_addr: list[int], io_data: list[int]):
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

    def get_meminfo(self, start: int = 0, end: int = 0):
        mem_info: str = ""
        with open(self.data_mem_path, 'rb') as f:
            byte_data = f.read()
            if end == 0: end = len(byte_data)
            # Вывод таблицы
            mem_info += "  Addr |  0  1  2  3 |  4  5  6  7 |  8  9 10 11 |\n"
            mem_info += "  -----|-------------|-------------|-------------|\n"

            for i in range(start, end, 12):
                # Адрес в шестнадцатеричном формате
                addr = i
                # Получаем до 12 байт для текущей строки
                chunk = byte_data[i:i + 12]
                # Форматируем байты в строку, разбивая на чанки по 4 байта
                bytes_str = []
                for j in range(12):
                    if j < len(chunk):
                        bytes_str.append(f"{chunk[j]:02X}")
                    else:
                        bytes_str.append("  ")  # Пробелы для недостающих байт
                # Разделяем на три чанка по 4 байта
                group1 = " ".join(bytes_str[0:4])
                group2 = " ".join(bytes_str[4:8])
                group3 = " ".join(bytes_str[8:12])
                # Выводим строку
                mem_info += f"  {addr:04X} | {group1: <10} | {group2: <10} | {group3: <10} |"
                mem_info += "\n"
        return mem_info

    def _sync_to_file(self):
        with open(self.data_mem_path, 'wb') as f:
            f.write(self.mem)

    def write(self, address: int, value: int) -> None:
        value = ltbe(value)
        if address <= self.size - 4:
            if address == self.output:
                self.output_stream.append(value)
            # Записываем 32-битное слово в big-endian
            for i in range(4):
                self.mem[address + i] = (value >> (24 - i * 8)) & 0xFF
            self._sync_to_file()
        else:
            raise ValueError("Attempting to write memory out of address space")

    def read(self, address: int) -> int:
        if address <= self.size - 4:
            if address == self.input:
                ret = self.input_stream[0]
                self.input_stream.pop(0)
                return tsfb(btle(ret))
            # Читаем 32-битное слово в big-endian
            ret = 0
            for i in range(4):
                ret |= self.mem[address + i] << (24 - i * 8)
            return tsfb(btle(ret))
        else:
            raise ValueError("Attempting to read memory out of address space")
