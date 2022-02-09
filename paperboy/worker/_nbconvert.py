import os
import os.path
import subprocess
import sys

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


def run(nb_name, nb_text, to="html", template="", hide_input=False):
    """Helper function to run nbconvert, used by airflow

    Args:
        nb_name (string): Name of notebook
        nb_text (string): nbformat json of text of notebook to convert
        to (string): what to convert to, options dictated by nbconvert
        template (string): path to template to use
        hide_input (boolean): hide code
    Returns:
        string: text/binary output of nbconvert
    """

    with TemporaryDirectory() as tempdir:
        in_file = os.path.join(tempdir, "{}.ipynb".format(nb_name))
        out_file = os.path.join(tempdir, "{}_out".format(nb_name))

        # hack for pdfs, .pdf appended automatically by xelatex
        if to != "pdf":
            out_file += "." + to

        with open(in_file, "w") as fp:
            fp.write(nb_text)

        # assemble nbconvert command
        argv = []
        argv = [sys.executable, "-m", "nbconvert", "--to", to]

        # pass in template arg
        if template:
            argv.extend(["--template", template])
        if hide_input:
            argv.append("--no-input")
        argv.append("--no-prompt")

        # output to outname
        argv.extend([in_file, "--output", out_file])

        subprocess.call(argv)

        # hack for pdfs
        if to == "pdf":
            out_file += "." + to

        # fail if doesnt exist
        with open(out_file, "rb") as fp:
            ret = fp.read()
    return ret
