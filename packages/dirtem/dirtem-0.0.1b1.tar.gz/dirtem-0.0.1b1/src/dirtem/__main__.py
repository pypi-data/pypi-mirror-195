import argparse
from importlib.metadata import version
from wcmatch.pathlib import Path

from . import build

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version",
    action = "version",
    version = f"%(prog)s {version('dirtem')}",
    help = "Displays the version of dirtem."
)
parser.add_argument("--config",
    type = Path,
    default = None,
    help = "Specify the path of the configuration file. Defaults to dirtem.toml in the same directory as `source`.")

#subparsers = parser.add_subparsers()
#parser_build = subparsers.add_parser("build")

parser.add_argument("source", type = Path, help = "Specify the path of the template directory.")
parser.add_argument("destination", type = Path, help = "Specify the path of the destination directory.")

args = parser.parse_args()
build(
    args.source,
    args.destination,
    args.config or (args.source.parent / "dirtem.toml"),
)
