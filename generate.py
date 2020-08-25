#!/usr/bin/env python3

import os
import sys
import yaml

from redashAPI import RedashAPIClient


USAGE = """
    Usage: ./generate.py path/to/template.yaml
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

    full_width_chart_count = 0
    # Create charts for each query and corresponding graph
    for index, chart in enumerate(template["charts"]):
        print(f'Creating chart {chart["title"]}...')

        query = \
            rd.create_query(
                BIGQUERY_SOURCE,
                chart["title"],
                chart["query"]).json()

        if isinstance(chart["y_axis"], list):
            axis_y = [{"name": name} for name in chart["y_axis"]]
        else:
            axis_y = [{"name": chart["y_axis"]}]
        graph = \
            rd.create_visualization(
                query["id"],
                chart["type"],
                "Chart",
                x_axis=chart["x_axis"],
                y_axis=axis_y,
                group_by=chart.get("group_by"),
                custom_options={
                    "xAxis": {
                        "type": "Auto Detect",
                        "labels": {"enable": True}
                    },
                    "showDataLabels": chart.get("show_data_labels", False)
                }
            ).json()

        is_full_width = chart.get("full_width", False)
        pos = calc_position(index, is_full_width, full_width_chart_count)
        rd.add_widget(
            dashboard_id,
            vs_id=graph["id"],
            position=pos
        )
        # Increment this counter after the widget gets added to the dashboard
        if is_full_width:
            full_width_chart_count += 1

    # Publish dashboard
    print("Publishing dashboard...")
    rd.publish_dashboard(dashboard_id)
    print("Done")


def calc_position(index, full_width, full_width_chart_count):
    """ Need to manually calculate the position as it's broken in `add_widget`.
    """
    position = {
        "col": 0,
        "row": 0,
        "sizeX": 3,  # default width is 3 units, full_width is 6 units
        "sizeY": 8   # default height is 8 units
    }

    row, col = divmod(index - full_width_chart_count, 2)
    position["row"] = (row + full_width_chart_count) * 8
    position["col"] = col * 3

    if full_width:
        position["sizeX"] = 6

    return position


if __name__ == '__main__':
    main()
