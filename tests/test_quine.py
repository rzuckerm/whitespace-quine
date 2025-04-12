import os
import subprocess
from pathlib import Path

from src import whitespace_quine

DOCKER_IMAGE = "esolang/whitespace:latest"
WHITESPACE_RUNNER = ["whitespace"]
WHITESPACE_TIMEOUT_SEC = 60


def test_quine():
    whitespace_quine.main()
    pwd = os.getcwd()
    with open(os.devnull, mode="r") as dev_null:
        actual = subprocess.run(
            ["docker", "run", "-i", "--rm", "-v", f"{pwd}:/local", "-w", "/local", DOCKER_IMAGE]
            + WHITESPACE_RUNNER
            + [whitespace_quine.ASSEMBLED_FILENAME],
            text=True,
            encoding="utf-8",
            stdin=dev_null,
            capture_output=True,
            timeout=WHITESPACE_TIMEOUT_SEC,
            check=True,
        ).stdout
    expected = Path(whitespace_quine.ASSEMBLED_FILENAME).read_text(encoding="utf-8")
    assert actual == expected
