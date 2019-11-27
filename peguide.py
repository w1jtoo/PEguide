import argparse
from src.PEGCore import Core


def main():
    parser = argparse.ArgumentParser(
        description="Show the structure of portable executable (PE) files under\
             the Windows family of operating systems. ",
        usage="peguide.py [part] file",
    )
    parser.add_argument("file")

    args = parser.parse_args()
    core = Core(args.file)
    core.read_headers()
    core.write_headers()


if __name__ == "__main__":
    main()
