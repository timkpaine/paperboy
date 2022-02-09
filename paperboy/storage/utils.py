from nbstripout import strip_output


def strip_outputs(nb):
    """Helper wrapper around nbstripout to remove notebook outputs"""
    return strip_output(nb, False, False)
