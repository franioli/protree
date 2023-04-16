import argparse
import os
import subprocess
import sys
from pathlib import Path

DEBUG = True


def parse_command_line() -> dict:
    """
    parse_command_line Parse command line input

    """
    parser = argparse.ArgumentParser(description="""Run Potree Converter.""")

    parser.add_argument("-i", "--source", help="Input file(s)", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory", required=True)
    parser.add_argument(
        "--encoding",
        help="Encoding type",
        type=str,
        choices=["BROTLI", "UNCOMPRESSED"],
        default="UNCOMPRESSED",
    )
    parser.add_argument(
        "-m",
        "--method",
        help="Point sampling method",
        type=str,
        choices=["poisson", "poisson_average", "random"],
        default="poisson",
    )
    parser.add_argument("--chunkMethod", help="Chunking method")
    parser.add_argument(
        "--keep-chunks",
        help="Skip deleting temporary chunks during conversion",
        action="store_true",
    )
    parser.add_argument(
        "--no-chunking", help="Disable chunking phase", action="store_true"
    )
    parser.add_argument(
        "--no-indexing", help="Disable indexing phase", action="store_true"
    )
    parser.add_argument(
        "--attributes", help="Attributes in output file", action="store_true"
    )
    parser.add_argument(
        "--projection",
        type=str,
        help="Add the projection of the pointcloud to the metadata",
    )
    parser.add_argument("--title", help="Page title used when generating a web page")

    args = parser.parse_args()

    input_dict = {
        "source": Path(args.source),
        "outdir": Path(args.outdir),
        "encoding": args.encoding,
        "method": args.method,
        "chunkMethod": args.chunkMethod,
        "keepChunks": args.keep_chunks,
        "noChunking": args.no_chunking,
        "noIndexing": args.no_indexing,
        "attributes": args.attributes,
        "projection": args.projection,
        "title": args.title,
    }

    return input_dict


def create_default_cfg() -> dict:
    cfg = {
        "source": "",
        "outdir": Path("output"),
        "encoding": "UNCOMPRESSED",
        "method": "poisson",
        "chunkMethod": None,
        "keepChunks": None,
        "noChunking": None,
        "noIndexing": None,
        "attributes": None,
        "projection": None,
        "generatePage": None,
        "title": None,
    }
    return cfg


def check_os() -> str:
    if sys.platform == "win32":
        return "win"
    elif sys.platform == "linux":
        return "linux"
    elif sys.platform == "darwin":
        return "macos"
    else:
        raise OSError("Unsupported OS")


def get_potree_converter_path() -> Path:
    os = check_os()
    project_root = Path(__file__).parents[1]
    if os == "win":
        path = project_root / "PotreeConverter.exe"
    if os == "linux":
        path = project_root / "PotreeConverter"
    if os == "macos":
        path = project_root / "PotreeConverter"
    assert path.exists(), f"{path.name} not found in {project_root} folder."
    return path


if __name__ == "__main__":

    # Get path to PotreeConverter and create default config
    pc_path = get_potree_converter_path()
    cfg = create_default_cfg()

    # Parse command line arguments and update config
    if not DEBUG:
        cmd_args = parse_command_line()
    else:
        cmd_args = {"source": "data/pcd.las", "outdir": "output"}
    cfg.update(cmd_args)
    cfg["outdir"] = Path(cfg["outdir"]).resolve()

    # run PotreeConverter
    print("Building Potree...")

    pc_outdir = cfg["outdir"] / "assets/pointclouds"
    pc_outdir.mkdir(parents=True, exist_ok=True)
    cmd = [pc_path, "-i", cfg["source"], "-o", pc_outdir]
    if cfg["encoding"]:
        cmd.extend(["-e", cfg["encoding"]])
    if cfg["method"]:
        cmd.extend(["-m", cfg["method"]])
    if cfg["chunkMethod"]:
        cmd.extend(["--chunkMethod", cfg["chunkMethod"]])
    if cfg["keepChunks"]:
        cmd.extend(["--keep-chunks"])
    if cfg["noChunking"]:
        cmd.extend(["--no-chunking"])
    if cfg["noIndexing"]:
        cmd.extend(["--no-indexing"])
    if cfg["attributes"]:
        cmd.extend(["--attributes"])
    if cfg["projection"]:
        cmd.extend(["--projection", cfg["projection"]])

    ret = subprocess.run(cmd)
    if ret.returncode != 0:
        raise RuntimeError("PotreeConverter failed.")

    print("Done.")
