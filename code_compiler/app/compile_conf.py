from code_compiler.config.config import instruction_file
import yaml


with open(instruction_file, 'r') as f:
    data = yaml.safe_load(f)["commands"]
    commands = {cmd["desc"]: cmd.get("operand", False) for cmd in data}

forbidden_var = ["a", "b", "var", "dup", "drop", "HALT"]

built_in_words = {
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "v+": "v+",
    "v-": "v-",
    "dup": "dup",
    "drop": "pop",
    "HALT": "halt",
}

