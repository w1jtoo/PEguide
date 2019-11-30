import argparse
from src.PEGCore import Core


def main():
    parser = argparse.ArgumentParser(
        description="Show the structure of portable executable (PE) files under\
             the Windows family of operating systems. ",
        usage="peguide.py <command> [part] file",
    )
    parser.add_argument("file")

    parser.add_argument(
        "--sections", nargs="?", const=True, default=False,
    )
    parser.add_argument(
        "--headers", nargs="?", const=True, default=False,
    )
    parser.add_argument(
        "--tables", nargs="?", const=True, default=False,
    )

    args = parser.parse_args()

    core = Core(args.file)
    core.read_headers()
    core.read_sections()
    core.read_directories()

    if args.headers:
        core.write_headers()
    if args.sections:
        core.write_sections()
    if args.tables:
        core.write_tables()
    if not (args.headers or args.sections or args.tables):
        core.write_headers()
        core.write_sections()
        core.write_tables()


if __name__ == "__main__":
    main()
