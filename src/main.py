"""Entry point: python src/main.py <perintah>"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from taskmanager.cli import run  # noqa: E402

if __name__ == "__main__":
    sys.exit(run())
