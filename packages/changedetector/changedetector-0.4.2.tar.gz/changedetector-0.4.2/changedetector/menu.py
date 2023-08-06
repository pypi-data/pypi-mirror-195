import sys
import inquirer
from rich import print as rprint
from wrapperComponents import WrapperComponents as wp
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(BASE_DIR, "themes")
THEME = os.path.join(THEMES_DIR, "inquirer.json")

def read_file(file_path: str) -> list:
    """
    Reads a file and returns a list of lines.
    :param file_path: The path to the file.
    :return: A list of lines.
    """
    with open(file_path, "r") as file:
        return file.read()

def menu(options:list, title:str, key:str):
    """
    A simple menu for the user to choose from.
    :param options: The options the user can choose from.
    :param title: The title of the menu.
    :return: The option the user chose.
    """
    inquirer.themes.load_theme_from_json(read_file(THEME))
    
    try:
        res = inquirer.prompt(
            [
                inquirer.List(
                    key,
                    message=title,
                    choices=options,
                    carousel=True
                )
            ]
        )[key]

    except Exception as e:
        rprint(f"{wp.textWrapBold('An error occured: ', 'red')}{wp.textWrap(e, 'red')}")
        rprint(f"{wp.textWrapBold('Exiting program...', 'red')}")
        sys.exit(1)
    return res

if __name__ == "__main__":
    MODE = menu(["Watch and Run Self (WRS)", "Watch and Run Other (WRO)"],
            "Choose the mode you want to use", "mode")
    print(MODE)

