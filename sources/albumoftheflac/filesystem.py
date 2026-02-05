# Standard
import os
import subprocess

def change_directory(path: str) -> None:
    try:
        subprocess.run(["cd", path])
    except Exception as e:
        raise Exception(f"There was a problem with changing the directory: {e}")

def delete_file(path: str) -> None:
    os.remove(path)
