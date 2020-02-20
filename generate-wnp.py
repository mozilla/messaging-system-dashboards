#!/usr/bin/env python3

import os
import sys
import yaml

from redashAPI import RedashAPIClient


USAGE = """
    Usage: ./generate-wnp path/to/template.yaml
"""

STMO = "https://sql.telemetry.mozilla.org"
BIGQUERY_SOURCE = 63


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        template = yaml.load(f, yaml.FullLoader)

    rd = RedashAPIClient(os.environ['REDASH_API_KEY'], STMO)

    # Create the dashboard
    print(f'Creating dashboard {template["title"]}...')
    dashboard = rd.create_dashboard(template["title"]).json()
    dashboard_id = dashboard["id"]

    # Create charts for each query and corresponding graph
    for index, chart in enumerate(template["charts"]):
        print(f'Creating chart {chart["title"]}...')
        query = \
            rd.create_query(
                BIGQUERY_SOURCE,
                chart["title"],
                chart["query"]).json()
        graph = \
            rd.create_visualization(
                query["id"],
                chart["type"],
                "Chart",
                x_axis=chart["x_axis"],
                y_axis=[{
                    "name": chart["y_axis"],
                    "label": "actions"
                }],
                group_by=chart["group_by"],
                custom_options={
                    "xAxis": {
                        "type": "Auto Detect",
                        "labels": {"enable": True}
                    }
                }
            ).json()
        rd.add_widget(
            dashboard_id,
            vs_id=graph["id"],
            position=calc_position(index)
        )

    # Publish dashboard
    print("Publishing dashboard...")
    rd.publish_dashboard(dashboard_id)
    print("Done")


def calc_position(index):
    """ Need to manually calculate the position as it's broken in `add_widget`.
    """
    position = {
        "col": 0,
        "row": 0,
        "sizeX": 3,
        "sizeY": 8
    }

    row, col = divmod(index, 2)
    position['row'] = row * 8
    position['col'] = col * 3

    return position


if __name__ == '__main__':
    main()
