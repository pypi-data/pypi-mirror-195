from netbox import NetBoxClient
import pandas as pd
from tabulate import tabulate
from typing import List
from enum import Enum
import json
import yaml


class ListFormat(str, Enum):
    text = "text"
    json = "json"
    yaml = "yaml"
    csv = "csv"


class TableFormat(str, Enum):
    plain = "plain"
    simple = "simple"
    github = "github"
    grid = "grid"
    simple_grid = "simple_grid"
    rounded_grid = "rounded_grid"
    heavy_grid = "heavy_grid"
    mixed_grid = "mixed_grid"
    double_grid = "double_grid"
    fancy_grid = "fancy_grid"
    outline = "outline"
    simple_outline = "simple_outline"
    rounded_outline = "rounded_outline"
    heavy_outline = "heavy_outline"
    mixed_outline = "mixed_outline"
    double_outline = "double_outline"
    fancy_outline = "fancy_outline"
    pipe = "pipe"
    orgtbl = "orgtbl"
    asciidoc = "asciidoc"
    jira = "jira"
    presto = "presto"
    pretty = "pretty"
    psql = "psql"
    rst = "rst"
    mediawiki = "mediawiki"
    moinmoin = "moinmoin"
    youtrack = "youtrack"
    html = "html"
    unsafehtml = "unsafehtml"
    latex = "latex"
    latex_raw = "latex_raw"
    latex_booktabs = "latex_booktabs"
    latex_longtable = "latex_longtable"
    textile = "textile"
    tsv = "tsv"


class BaseCrudCommand:
    connection = NetBoxClient(
        base_url="http://127.0.0.1:8000/",
        token="1dc6fa5bfcef8390dd83a261c36ed8f1551b2d6b",
    )

    def list(self, format: ListFormat, columns: str, indent: int, tablefmt: TableFormat):
        data = self.base_api.list().data["results"]
        if format == ListFormat.text:
            data = pd.json_normalize(data, sep="__")
            columns = columns.split(",")
            data = data[data.columns.intersection(columns)]
            print(tabulate(data, headers="keys", tablefmt=tablefmt, showindex=False))
            return

        if format == ListFormat.json:
            print(json.dumps(data, indent=indent))
            return

        if format == ListFormat.yaml:
            print(yaml.dump(data))
            return

        if format == ListFormat.csv:
            data = pd.json_normalize(data, sep="__")
            columns = columns.split(",")
            print(data.to_csv(index=False, columns=columns))
            return

    def get(self, func):
        pass

    def create(self, func):
        pass

    def update(self, func):
        pass

    def delete(self, func):
        pass
