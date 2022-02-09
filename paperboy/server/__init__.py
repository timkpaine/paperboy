import sys


def main():
    """Use gunicorn on linux or waitress on windows to deplot a
    paperboy instance"""
    from ..config.application import Paperboy

    Paperboy.launch_instance(sys.argv)
