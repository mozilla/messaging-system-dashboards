#!/usr/bin/env python3

import sys
import yaml

from jinja2 import Environment, FileSystemLoader


USAGE = """
    Usage:
        ./generate_template.py config.yaml meta_template.py out.yaml

    Example:
        ./generate_template.py templates/cfr_template_config.yaml cfr.template.yaml templates/cfr/out.yaml
"""


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        config = yaml.load(f, yaml.FullLoader)

    env = Environment(
        loader=FileSystemLoader("./templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(sys.argv[2])

    with open(sys.argv[3], "w") as f:
        f.write(template.render(config))
