import typer

from cwbtasks import __app_name__, __version__

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of tasks application"""
    print(f"{__app_name__} v{__version__}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Tasks is a small command line task tracking application.
    """
    return
