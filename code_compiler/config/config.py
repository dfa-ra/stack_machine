import os

import yaml

wd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(wd, 'config.yaml')) as config_file:
    cfg = yaml.safe_load(config_file)

build_dir = wd + "/" + cfg['BUILD_DIR']

os.makedirs(os.path.dirname(build_dir), exist_ok=True)
