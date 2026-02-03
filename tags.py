# Standard
import aiofiles
import subprocess

def export_tags(text_file: str) -> None:
    try:
        subprocess.run(["metaflac", f"--export-tags-to={text_file}", "*.flac"])
    except Exception as e:
        raise f"There was a problem with exporting tags: \n{e}"

async def read_tags_from_file(text_file: str) -> str:
    async with aiofiles.open(text_file, "r") as file:
        return await f.read()

def get_tag(tags_from_file: str, tag: str):
    for line in tags_from_file:
        if tag in line:
            return line.split(tag)
