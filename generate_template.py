#!/usr/bin/env python3

import sys
import yaml

from jinja2 import Environment, FileSystemLoader


USAGE = """
    Usage:
        ./generate_template.py [cfr|wnp|onboarding] path/to/output.yaml

    Example:
        ./generate_template.py cfr templates/cfr/output.yaml
"""

TEMPLATE_PATHS = {
    "cfr": ("cfr_template_config.yaml", "cfr.yaml.template")
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    if sys.argv[1] not in TEMPLATE_PATHS:
        print("Invalid template type '{}', "
              "it must be one of 'cfr', 'wnp', and 'onboarding'"
              .format(sys.argv[1]))
        sys.exit(1)

    config_file, template_file = TEMPLATE_PATHS.get(sys.argv[1])

    with open(config_file, "r") as f:
        config = yaml.load(f, yaml.FullLoader)

    env = Environment(
        loader=FileSystemLoader("./templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(template_file)

    with open(sys.argv[2], "w") as f:
        f.write(template.render(config))
