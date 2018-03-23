# coding: utf-8

r"""Utilities to group a STEP file and an anchors file in a zip file"""

import logging

from os.path import basename, splitext, dirname, join
import zipfile

logger = logging.getLogger(__name__)


def create_stepzip(step_file, anchors_file):
    r"""Procedure to create a zip file from a STEP file and an anchors file

    Parameters
    ----------
    step_file : str
        Path to the STEP file
    anchors_file : str
        Path to the anchors file

    """
    zf = zipfile.ZipFile("%s/%s.zip" % (dirname(step_file),
                                        basename(splitext(step_file)[0])),
                         "w",
                         zipfile.ZIP_DEFLATED)
    zf.write(step_file, basename(step_file))
    zf.write(anchors_file, basename(anchors_file))
    zf.close()


def extract_stepzip(stepzip):
    r"""Extract the contents of a STEP + anchors zip file

    Parameters
    ----------
    stepzip : str
        Path to the STEP + anchors zip file

    Returns
    -------
    Tuple[str, str] : path to the STEP file, path to the anchors file

    """
    zip_ref = zipfile.ZipFile(stepzip)
    step_file_path, anchors_file_path = None, None

    if len(zip_ref.namelist()) != 2:
        msg = "The zip file should contain 2 files"
        raise ValueError(msg)

    for name in zip_ref.namelist():
        # bname, ext = splitext(name)
        _, ext = splitext(name)
        if ext in [".stp", ".step", ".STP", ".STEP"]:
            step_file_path = join(dirname(stepzip), name)
        else:
            anchors_file_path = join(dirname(stepzip), name)
    zip_ref.extractall(dirname(stepzip))
    zip_ref.close()
    return step_file_path, anchors_file_path
