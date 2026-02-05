# Standard
import subprocess
from pathlib import Path


def export_tags() -> str:
    try:
        flac_files = [str(f) for f in Path(".").glob("*.flac")]
        if not flac_files:
            raise RuntimeError("No FLAC files were found in this directory")

        command = ["metaflac", "--export-tags-to=-"] + [flac_files[0]]
        p = subprocess.run(command, text=True, capture_output=True)

        if p.returncode != 0:
            raise RuntimeError((p.stderr or "").strip() or "metaflac failed")

        return p.stdout if p.stdout is not None else ""

    except Exception as e:
        raise Exception(f"There was a problem with exporting tags: \n{e}")


def get_tag(tags: str, tag: str) -> str:
    tag = tag.upper()
    for line in tags:
        if tag in line:
            return line.split(tag)[1]

    return ""


def set_tag(tag_name: str, tag_content: str):
    try:
        subprocess.run(
            [
                "metaflac",
                f"--remove-tag={tag_name.upper()}",
                f'--set-tag="{tag_name.upper()}={tag_content}"',
                "*.flac",
            ]
        )
    except Exception as e:
        raise Exception(e)
