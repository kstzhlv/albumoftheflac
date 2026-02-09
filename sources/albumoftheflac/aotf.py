# Standard
import argparse
import asyncio
from pathlib import Path

# Local
from albumoftheflac.orchestrator import set_correct_tags


async def run_tags(directories):
    for sub_dir in directories:
        try:
            print(f"Processing {sub_dir}...")
            await set_correct_tags(sub_dir)

        except Exception as e:
            print(f"Failed to parse tags for {sub_dir}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="aotf",
        description="Retrieve genre and date tags \
                    from Album of the Year \
                    and set them to all flac files in the directory",
    )

    parser.add_argument("directory", type=str, help="Directory to parse")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively (default)",
    )

    group.add_argument(
        "-n",
        "--non-recursive",
        action="store_true",
        help="Process only the current directory",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    base_directory = Path(args.directory).resolve()

    if not base_directory.is_dir():
        raise ValueError(f"{base_directory} is not a directory")

    if args.non_recursive:
        directories_to_process = [base_directory]

    else:
        directories_to_process = [
            d for d in base_directory.rglob("*") if d.is_dir() and any(d.glob("*.flac"))
        ]

    asyncio.run(run_tags(directories_to_process))


if __name__ == "__main__":
    main()
