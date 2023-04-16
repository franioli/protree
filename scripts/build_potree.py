import argparse
import os
import subprocess
import sys
import logging
from pathlib import Path

DEBUG = True


def init_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_dir / "build_potree.log"),
            logging.StreamHandler(),
        ],
    )


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
    parser.add_argument(
        "--quiet", help="Suppress console output", action="store_true", default=False
    )

    args = parser.parse_args()

    input_dict = {
        "source": Path(args.source).resolve(),
        "outdir": Path(args.outdir).resolve(),
        "encoding": args.encoding,
        "method": args.method,
        "chunkMethod": args.chunkMethod,
        "keepChunks": args.keep_chunks,
        "noChunking": args.no_chunking,
        "noIndexing": args.no_indexing,
        "attributes": args.attributes,
        "projection": args.projection,
        "title": args.title,
        "quiet": args.quiet,
    }

    return input_dict


def create_default_cfg() -> dict:
    cfg = {
        "source": "",
        "outdir": Path("output").resolve(),
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
        "quiet": False,
    }
    return cfg


if __name__ == "__main__":

    # Set up logging and get PotreeConverter path
    init_logging()
    cfg = create_default_cfg()
    pc_path = get_potree_converter_path()

    # Parse command line arguments and update config
    if not DEBUG:
        cmd_args = parse_command_line()
    else:
        cmd_args = {"source": "data/pcd.las", "outdir": "output", "quiet": False}
        cmd_args["outdir"] = Path(cmd_args["outdir"])
    cfg.update(cmd_args)

    # run PotreeConverter
    logging.info("Building Potree...")

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

    if not cfg["quiet"]:
        ret = subprocess.run(cmd)
    else:
        ret = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ret.returncode != 0:
        raise RuntimeError("PotreeConverter failed.")
    else:
        logging.info("PotreeConverter completed successfully.")

    # Build Potree page
    logging.info("Building Potree page...")

    logging.info("Done.")
