import os
import os.path
import subprocess
from tempfile import NamedTemporaryFile
from venv import create


def create_virtualenv(requirements_txt, directory):
    """Helper function to create a virtualenv from a requirements.txt file

    Args:
        requirements_txt (string): text of requirements.txt to use to build virtualenv
        directory (string): directory directory of created base virtualenv
    Returns:
        None
    """
    create(directory, with_pip=True)

    source = os.path.join(directory, "bin", "activate")
    with NamedTemporaryFile(suffix="txt") as fp:
        fp.write(requirements_txt.encode("utf-8"))
        command = ["source", source, "&&", "pip", "install", "-r", fp.name]
        subprocess.call(command)
