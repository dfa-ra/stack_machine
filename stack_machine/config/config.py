import os

import yaml

wd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(wd, 'config.yaml')) as config_file:
    cfg = yaml.safe_load(config_file)

log_file = wd + "/" + cfg['LOG_FILE']
instruction_file = wd + "/" + cfg['INSTRUCTION_FILE']
microcode_mem_file = wd + "/" + cfg["MICRO_COMMAND_MEM_PATH"] + "microcode.bin"
op_table_file = wd + "/" + cfg["MICRO_COMMAND_MEM_PATH"] + "op_table.yaml"
source_mc_file = wd + "/" + cfg["SOURCE_MC_FILE"]

instruction_mem_path = wd + "/" + cfg["INSTRUCTION_MEM_PATH"] + "instruction_memory.bin"
data_mem_path = wd + "/" + cfg["DATA_MEM_PATH"] + "data_memory.bin"
