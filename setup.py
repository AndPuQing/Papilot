from rich.console import Console
from rich.table import Table
from rich import box
from papilot.config import *
from dotenv import set_key, dotenv_values

env_dist = os.environ
LOGO = "  ██████╗  █████╗ ██████╗ ██╗██╗      ██████╗ ████████╗\n" \
       "  ██╔══██╗██╔══██╗██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝\n" \
       "██████╔╝███████║██████╔╝██║██║     ██║   ██║   ██║   \n" \
       "██╔═══╝ ██╔══██║██╔═══╝ ██║██║     ██║   ██║   ██║   \n" \
       "██║     ██║  ██║██║     ██║███████╗╚██████╔╝   ██║   \n" \
       "╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝   \n"

MODELS = [
    "codegen-350M-mono 2GB Python-only",
    "codegen-350M-multi 2GB multi-language",
    "codegen-2B-mono 7GB Python-only",
    "codegen-2B-multi 7GB multi-language",
    "codegen-6B-mono 13GB Python-only",
    "codegen-6B-multi 13GB multi-language",
    "codegen-16B-mono 32GB Python-only",
    "codegen-16B-multi 32GB multi-language"
]

console = Console()
console.print(LOGO, justify="center", style="bold red")
console.print("[bold blue]An open-source GitHub Copilot server based PaddleNLP", justify="center")

# Model selection
MODELS_TABLE = Table(title="Models available", box=box.SIMPLE_HEAD, show_header=True, header_style="bold yellow")
MODELS_TABLE.add_column("ID", style="bold yellow")
MODELS_TABLE.add_column("Model", style="bold yellow")
MODELS_TABLE.add_column("VRAM", style="bold yellow")
MODELS_TABLE.add_column("Languages", style="bold yellow")
for i, model in enumerate(MODELS):
    MODELS_TABLE.add_row(str(i + 1), model.split(" ")[0], model.split(" ")[1], model.split(" ")[2])
console.print(MODELS_TABLE)

modelIn = console.input("[green bold]Select model \\[default: 1]: ")
if modelIn.isdigit():
    set_key(dotenv_path="config.env", key_to_set="MODEL",
            value_to_set="Salesforce/" + MODELS[int(modelIn) - 1].split(" ")[0])
else:
    set_key(dotenv_path="config.env", key_to_set="MODEL",
            value_to_set="Salesforce/codegen-350M-mono")

# GPU selection
gpus = console.input("[green bold]Enter number of GPUs \\[default: 1]: ")
if gpus.isdigit():
    set_key(dotenv_path="config.env", key_to_set="NUM_GPUS", value_to_set=gpus)
else:
    set_key(dotenv_path="config.env", key_to_set="NUM_GPUS", value_to_set="1")

# Deployment method selection
method_table = Table(title="Deploy method", box=box.SIMPLE_HEAD, show_header=True, header_style="bold yellow")
method_table.add_column("ID", style="bold yellow")
method_table.add_column("Method", style="bold yellow")
method_table.add_row("1", "Docker")
method_table.add_row("2", "localhost")
console.print(method_table)
method = console.input("[bold green]Where do you want to deploy the model? \\[default: localhost]: ")
if method.isdigit():
    set_key(dotenv_path="config.env", key_to_set="DEPLOY_METHOD",
            value_to_set="Docker" if int(method) == 1 else "localhost")
else:
    set_key(dotenv_path="config.env", key_to_set="DEPLOY_METHOD", value_to_set="localhost")

# Port selection
port = console.input("[bold green]Enter port \\[default: 8000]: ")
if port.isdigit():
    set_key(dotenv_path="config.env", key_to_set="PORT", value_to_set=port)
else:
    set_key(dotenv_path="config.env", key_to_set="PORT", value_to_set="8000")

# Print config
console.print("[bold green]Configuration completed...")
config = dotenv_values(dotenv_path="config.env")
config_table = Table(title="Configuration", box=box.SIMPLE_HEAD, show_header=True, header_style="bold yellow")
config_table.add_column("Key", style="bold yellow")
config_table.add_column("Value", style="bold yellow")
for key, value in config.items():
    config_table.add_row(key, value)
console.print(config_table)
