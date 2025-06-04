import yaml
import struct
from pathlib import Path

from stack_machine.cpu.micro_command.micro_command_description import mc_sigs_info
from stack_machine.config.config import microcode_mem_file, op_table_file, source_mc_file


def encode_mc(signal_groups: list[dict]) -> int:
    result = 0
    for group in signal_groups:
        unit = group["unit"]
        signals = group["signals"]
        info = mc_sigs_info[unit]
        base = info.bit_range[0]
        for sig in signals:
            offset = info.signals[sig]
            result |= 1 << (base + offset)
    return result


def compile_yaml_to_bin(yaml_path: Path, out_bin_path: Path, out_table_path: Path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    microcode_bin = []
    op_table = {}
    curr_addr = 0

    for cmd in data["commands"]:
        opcode = int(cmd["opcode"], 0)
        micro_commands = cmd["micro_commands"]
        op_table[opcode] = curr_addr

        for mc in micro_commands:
            print(mc)
            word = encode_mc(mc["signals"])
            microcode_bin.append(word)
            curr_addr += 1

    out_bin_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_bin_path, "wb") as f:
        for word in microcode_bin:
            f.write(struct.pack("<I", word))  # little-endian uint32

    with open(out_table_path, "w") as f:
        yaml.dump({"op_table": op_table}, f)


def compile_micro_command():
    compile_yaml_to_bin(Path(source_mc_file), Path(microcode_mem_file), Path(op_table_file))


if __name__ == "__main__":
    compile_micro_command()
