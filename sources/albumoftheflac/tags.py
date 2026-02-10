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
    for line in tags.upper().splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        if tag == k:
            return v
    return ""


def set_tag(album_dir: Path, tag_name: str, tag_content: str):
    flac_files = list(album_dir.glob("*.flac"))
    if not flac_files:
        raise RuntimeError("No FLAC files were found")

    tag = tag_name.upper()

    command = ["metaflac", f"--remove-tag={tag}", f"--set-tag={tag}={tag_content}"] + [
        str(f) for f in flac_files
    ]

    p = subprocess.run(command, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "metaflac failed")
