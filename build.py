from argparse import ArgumentParser
import subprocess

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--lib",
        action="extend",
        nargs="+",
        type=str,
    )
    args = parser.parse_args()

    if args.lib:
        subprocess.run(["beet", "-s", f'"broadcast = {args.lib}"'])
    else:
        subprocess.run(["beet"])
