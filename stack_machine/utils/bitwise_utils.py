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
    mask = (1 << bit_length) - 1
    num = num & mask

    sign_bit = 1 << (bit_length - 1)
    if num & sign_bit:
        complement = ((~num & mask) + 1) & mask
        return -complement
    else:
        return num
