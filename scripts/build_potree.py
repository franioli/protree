import os
import parser
import subprocess
import sys
from pathlib import Path


def parse_command_line_args() -> dict:
    pass


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
        assert path.exists(), f"PotreeConverter.exe not found in {project_root} folder."
    if os == "linux":
        path = project_root / "PotreeConverter"
        assert path.exists(), f"PotreeConverter not found in {project_root} folder."
    if os == "macos":
        path = project_root / "PotreeConverter"
        assert path.exists(), f"PotreeConverter not found in {project_root} folder."

    return path


if __name__ == "__main__":
    pc_path = get_potree_converter_path()

    print("Building Potree...")

    print("Done.")
