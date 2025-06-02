def get_signal_bit(signal: list[int], position: int) -> int:
    if position < 0:
        raise IndexError("Position must be non-negative")

    word_index = position // 32
    bit_offset = position % 32

    if word_index >= len(signal):
        raise IndexError(f"Position {position} exceeds signal length")

    return (signal[word_index] >> bit_offset) & 1


def set_signal_bit(signal: list[int], position: int, val: int):
    if position < 0:
        raise IndexError("Position must be non-negative")
    word_index = position // 32
    bit_offset = position % 32
    if word_index >= len(signal):
        raise IndexError(f"Position {position} exceeds signal length")
    if val == 1:
        signal[word_index] |= (val << bit_offset)
    else:
        signal[word_index] &= (val << bit_offset)


def set_signal_cut(signal: list[int], position: list[int], value: int):
    if len(position) == 1:
        set_signal_bit(signal, position[0], value & 0x1)
        return

    if value < 0:
        value = value & 0xffffffff

    start, end = position

    if start > end:
        raise IndexError("Invalid range: start > end")
    if start < 0 or end < 0:
        raise IndexError("Positions must be non-negative")
    if (end - start + 1) > 32:
        raise IndexError("Range cannot exceed 32 bits")

    mask = (1 << (end - start + 1)) - 1
    if value & ~mask:
        raise ValueError(f"Value {value} exceeds {end - start + 1} bits")

    for i in range(start, end + 1):
        word_index = i // 32
        bit_offset = i % 32
        bit = (value >> (i - start)) & 1

        if bit:
            signal[word_index] |= (1 << bit_offset)
        else:
            signal[word_index] &= ~(1 << bit_offset)


def get_signal_cut(signal: list[int], position: list[int]) -> int:
    if len(position) == 1:
        return get_signal_bit(signal, position[0])

    if len(position) != 2:
        raise ValueError("Position must be either int or tuple of two ints")

    start, end = position

    if start > end:
        raise IndexError("Invalid cut range: start > end")
    if start < 0 or end < 0:
        raise IndexError("Positions must be non-negative")
    if (end - start + 1) > 32:
        raise IndexError("Cut length cannot exceed 32 bits")

    result = 0
    for i in range(start, end + 1):
        word_index = i // 32
        bit_offset = i % 32

        if word_index >= len(signal):
            raise IndexError(f"Position {i} exceeds signal length")

        bit = (signal[word_index] >> bit_offset) & 1
        result |= (bit << (i - start))

    return result


def get_int_cut(src: int, pos: list[int]):
    if len(pos) == 1:
        return (src >> pos[0]) & 0x1
    mask = (1 << (pos[1] - pos[0] + 1)) - 1
    return (src >> pos[0]) & mask


def set_int_cut(src: int, pos: list[int], val: int) -> int:
    if val < 0:
        val = -val
        val |= 1 << (pos[1] - pos[0])
    if len(pos) == 1:
        mask = 1 << pos[0]
        return (src & ~mask) | ((val & 0x1) << pos[0])
    if len(bin(val)[2:]) > pos[1] - pos[0] + 1:
        raise ValueError(f"Value is longer than it's possible range: val: {val}, pos: {pos}")
    else:
        mask = (1 << (pos[1] - pos[0] + 1)) - 1
        shifted_mask = mask << pos[0]
        return (src & ~shifted_mask) | ((val & mask) << pos[0])


def cast_immediate(num: int, bit_range: list[int]) -> int:
    start, end = bit_range
    bit_length = end - start + 1

    # Получаем битовую длину числа (без ведущих нулей)
    num_bits = num.bit_length() if num != 0 else 0

    # Если число имеет такую же длину, как диапазон
    if num_bits == bit_length:
        # Обрезаем старший бит
        mask = (1 << (bit_length - 1)) - 1
        result = num & mask
        # Делаем число отрицательным
        return -result
    else:
        return num
