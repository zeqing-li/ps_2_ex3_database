import kaggle
import os
import json
from pathlib import Path
import click


def kaggle_api_key(
    user_name: str | None = None, api_key: str | None = None
) -> None:
    """
    Function that takes the kaggle API key as input and saves it to
    ~/.kaggle/kaggle.json if it doesn't exist
    """
    if user_name is not None and api_key is not None:
        # Create ~/.kaggle directory if it doesn't exist
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_dir.mkdir(parents=True, exist_ok=True)

        # Path to kaggle.json
        kaggle_json = kaggle_dir / "kaggle.json"

        # Create the JSON content
        api_config = {"username": user_name, "key": api_key}

        # Write the config file if it doesn't exist
        if not kaggle_json.exists():
            with open(kaggle_json, "w") as f:
                json.dump(api_config, f)

            # Set file permissions to be readable only by the user
            os.chmod(
                kaggle_json, 0o600
            )  # read and write permission only for the user
            print(f"Kaggle API key has been saved to {kaggle_json}")


def kaggle_download_data(dataset: str) -> None:
    """
    Function that downloads the NBA database from Kaggle
    """
    # Create the data directory if it doesn't exist
    root_path = Path(__file__).parent.parent
    data_path = root_path / "data"
    data_path.mkdir(parents=True, exist_ok=True)

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=data_path, unzip=True)
    print(f"Data has been downloaded to {data_path}")


@click.command()  # type: ignore
@click.option(  # type: ignore
    "--dataset",
    "-d",
    required=True,
    help='Kaggle dataset identifier (e.g., "username/dataset-name")',
)
@click.option(  # type: ignore
    "--user-name",
    "-u",
    required=False,
    help="Your Kaggle username",
)
@click.option(
    "--api-key", "-k", required=False, help="Your Kaggle API key"
)  # type: ignore
def main(
    dataset: str,
    user_name: str | None = None,
    api_key: str | None = None,
) -> None:
    kaggle_api_key(user_name=user_name, api_key=api_key)
    kaggle_download_data(dataset=dataset)


"""
The click package provides decorators and functions to simplify the creation of CLI commands. Here’s how it enables CLI functionality:

Command and Option Decorators:

@click.command() turns a Python function into a command-line command.
@click.option() defines options for the command, such as --dataset or --user-name, and specifies if they are required, have default values, or types. Each option corresponds to a parameter that users can provide when they execute the script.
Automatic Parsing:

click automatically parses the arguments and options provided in the command line, converting them into the specified data types and passing them as arguments to the function. This means users can simply enter --dataset <dataset-name>, and click will handle the rest.
Help Messages and Validation:

click generates help messages for each option (e.g., when running python script_name.py --help). It also validates input types and displays meaningful error messages if required options are missing or the input type is incorrect.
Chaining Commands:

click supports chaining commands, enabling more complex CLI tools with multiple commands and subcommands (similar to git or docker CLI structure).
"""


if __name__ == "__main__":
    main()
"""
serves as the entry point for the script.
In Python, if __name__ == "__main__": checks if the script is being run directly,
rather than being imported as a module in another script.
When the script is executed directly, __name__ is set to "__main__", which triggers the main() function to run.
This pattern is used to allow a Python file to act both as an importable module
(when it doesn’t execute any code upon import) and as an executable script.
In this case, it ensures that the main() function—configured as a command-line interface (CLI) with the click package—only runs when the file is executed directly.
"""
