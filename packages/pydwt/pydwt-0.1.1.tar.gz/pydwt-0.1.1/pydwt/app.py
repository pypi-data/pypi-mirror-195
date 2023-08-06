import traceback
from typing import Dict
import os
import sys
from typing import Optional
import typer
import yaml
from dependency_injector.wiring import register_loader_containers
from pydwt.core.containers import Container
import logging


sys.path.append(os.getcwd())
app = typer.Typer()
container = Container()
register_loader_containers(container)


def load_config(path: str) -> Dict:
    config = None
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


# Define command-line interface using Typer
@app.command()
def new(project_name: str):
    """Create a new pydwt project."""
    project_handler = container.project_factory()
    project_handler.new(project_name)


@app.command()
def run(name: Optional[str] = typer.Argument(None)):
    """Run the workflow DAG for the current project."""
    config = load_config(path="settings.yml")
    container.config.from_dict(config)
    project_handler = container.project_factory()
    project_handler.run(name)


@app.command()
def export_dag():
    """Export the workflow DAG for the current project."""
    config = load_config(path="settings.yml")
    container.config.from_dict(config)
    project_handler = container.project_factory()
    project_handler.export_dag()


@app.command()
def test_connection():
    """Export the workflow DAG for the current project."""
    config = load_config(path="settings.yml")
    container.config.from_dict(config)
    try:
        conn = container.database_client()
        engine = conn.get_engine()
        dbapi = engine.connect()
        dbapi.close()
        logging.info("successfully connected to db")
    except Exception:
        logging.error(f"connection failed {traceback.print_exc()}")


if __name__ == "__main__":
    # Run the command-line interface
    try:
        app()
    except Exception as e:
        # Display a helpful error message if a known error occurs
        if "config" in str(e):
            print("Error: Failed to load configuration from settings.yml.")
            print("Make sure the file exists and contains valid YAML data.")
        else:
            # Display the full error message for unknown errors
            print(f"Error: {e}")
