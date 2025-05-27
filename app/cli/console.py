#!/usr/bin/python3
"""
CLI Interface with Rich Presentation
"""
import typer
from rich.console import Console
from rich.prompt import Prompt
from app.core.agent import VehicleAgent

app = typer.Typer()
console = Console()
agent = VehicleAgent()


def display_vehicle(vehicle_data: str):
    """Rich-formatted vehicle display"""
    for block in vehicle_data.split("\n\n"):
        console.print("[bold]Vehicle Details[/bold]")
        for line in block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                console.print(f"  [cyan]{key.strip()}:[/cyan] {val.strip()}")


@app.command()
def interactive():
    """Interactive query session"""
    console.print("[bold green]Vehicle AI Agent[/] (type 'exit' to quit)")

    while True:
        try:
            query = Prompt.ask("\nAsk a question")
            if query.lower() in ('exit', 'quit'):
                break

            response = agent.query(query)
            display_vehicle(response)

        except KeyboardInterrupt:
            console.print("\n[red]Exiting...[/red]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    app()
