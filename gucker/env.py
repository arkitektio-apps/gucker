import os


GUCKER_PATH = os.path.dirname(os.path.realpath(__file__))
ASSETS_PATH = os.path.join(GUCKER_PATH, "assets")


def get_asset_file(file: str, darkMode: bool =False) -> str:
    """Gets the path to an asset file

    Args:
        file (str): The file name
        darkMode (bool, optional): Should we use the dark mode. Defaults to False.

    Returns:
        str: The path
    """
    return os.path.join(ASSETS_PATH, file)
