import typer

from cli.circuits import circuits

app = typer.Typer()
app.add_typer(circuits.app, name="circuits")

if __name__ == "__main__":
    app()
