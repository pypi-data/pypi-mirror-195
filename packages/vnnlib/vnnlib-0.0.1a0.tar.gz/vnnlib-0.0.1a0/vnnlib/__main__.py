import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        "vnnlib",
        description="",
    )
    parser.add_argument("file", nargs="+")
    return parser.parse_args()


def __main__():
    args = parse_args()
    print(f"parsing {args.file}")


if __name__ == "__main__":
    __main__()
