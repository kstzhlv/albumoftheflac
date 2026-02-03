# Standard
import subprocess

def change_directory(directory: str) -> None:
    try:
        subprocess.run(["cd", directory])
    except Exception as e:
        raise f"There was a problem with changing the directory. Maybe it does not exist.\n{e}"

