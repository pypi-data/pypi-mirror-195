import typer

from netbox import NetBoxClient
import pandas as pd
from tabulate import tabulate
from cli.crud import BaseCrudCommand, ListFormat, TableFormat
from typing import List


class CircuitTermination(BaseCrudCommand):
    @property
    def base_api(self):
        return self.connection.circuits.circuit_terminations


app = typer.Typer()


@app.command()
def list(
    format: ListFormat = typer.Option(ListFormat.json, prompt=True),
    columns: str = typer.Option("id"),
    indent: int = typer.Option(4),
    tablefmt: TableFormat = typer.Option(TableFormat.psql),
):
    CircuitTermination().list(format, columns, indent, tablefmt)


def get():
    CircuitTermination().get()


def create():
    CircuitTermination().create()


def update():
    CircuitTermination().update()


def delete():
    CircuitTermination().delete()
