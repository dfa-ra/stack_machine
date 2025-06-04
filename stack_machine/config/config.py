import os

import yaml
from typing import List
from stack_machine.cpu.micro_command import MicroCommand

wd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(wd, 'config.yaml')) as config_file:
    cfg = yaml.safe_load(config_file)

mc_config_path = cfg['MC_CONFIG_FILE']
log_file = cfg['LOG_FILE']
