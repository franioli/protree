import os
import subprocess
import sys
from pathlib import Path


def check_os() -> str:
    if sys.platform == "win32":
        return "win"
    elif sys.platform == "linux":
        return "linux"
    elif sys.platform == "darwin":
        return "macos"
    else:
        raise OSError("Unsupported OS")


def get_potree_converter_path(os: str) -> Path:
    return Path(__file__).parent.parent / "potree"


if __name__ == "__main__":

    print("Done.")
