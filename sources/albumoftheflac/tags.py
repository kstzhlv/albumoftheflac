# Standard
import subprocess
from pathlib import Path


def export_tags(album_dir: Path) -> str:
    try:
        flac_files = list(album_dir.glob("*.flac"))
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
    for line in tags.splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        print(f"DEBUGGING: tags.get_tag(): k: {k}, v: {v}, tag: {tag}")
        if tag == k:
            return v
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
