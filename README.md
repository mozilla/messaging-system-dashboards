Auto generate dashboard on Redash for User Journey

## Install

```sh
# This utility requires Python 3, highly recommended to use the virtual environment
$ virtualenv venv 
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Make sure get your Redash API key, it's available on Redash `Edit Profile -> Settings -> API Key`
# You can add it to your shell profile, such as `export REDASH_API_KEY="your_api_key"`.

```

## Usage

### Dashboard Template

Each dashboard is defined by a dashboard template file (YAML), which, in turn, is comprised of 
a title and a list of charts.

#### Define Chart

Each dashboard consists of multiple charts, and each chart can be defined as follows:

```yaml
title: "WNP 72: Badge Impression&Clicks"
type: line
query: |
  SELECT EXTRACT(date from submission_timestamp) as date,
   event,
   count(*) as count,
  FROM messaging_system.cfr
  WHERE EXTRACT(date FROM submission_timestamp) BETWEEN '2020-01-07' AND '2020-02-10'
    AND release_channel = 'release'
    AND version LIKE '72%'
    AND event in ('IMPRESSION', 'CLICK')
    AND message_id = 'WHATS_NEW_BADGE_72'
  GROUP BY 1, 2
x_axis: date
y_axis: count
group_by: event
```

Most properties are self-explained,
* The `query`, defined by the author, provides the input of this chart
* The `type` sets the chart type, it could be "line", "area", "bar", "pie", "scatter", "bubble", "box", "pivot", and "table"
* The `x_axis` and `y_axis` set the axes, they should be the columns from the SELECT statement in the `query`
* The x axis could be further broken down by the `group_by`.

### Generate Dashboard

Once the template is defined, you can generate a dashboard with the generator.

For instance, to generate a dashboard for the "What's New Panel".

```sh
$ ./generate-wnp.py templates/whats-new-panel.yaml
```

Then you can go to Redash, click on `Dashboards` on the top-left, you should find the new dashboard (already published) there.

Note that for each chart, there should be a new query crated on Redash, though it's not published. You can find them in the `Queries` section on Redash.
