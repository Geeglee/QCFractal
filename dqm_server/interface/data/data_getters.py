"""
Assists in grabbing the requisite data
"""

import copy
import json
import glob
import os

from ..molecule import Molecule
print("hr")

__all__ = ["list_directories", "get_file_name", "get_file", "get_molecule", "get_options"]

_data_dir = os.path.dirname(__file__)

_folders = ["molecules", "options"]
_data_folders = {x: os.path.join(_data_dir, x) for x in _folders}


def _get_folder_path(folder):
    if folder not in _data_folders:
        raise KeyError("Folder '%s' not recognized" % folder)

    return _data_folders[folder]


def list_directories():
    """
    List all known directories.
    """
    return copy.deepcopy(_data_folders.keys())


def get_file_name(folder, filename=None):
    folder = _get_folder_path(folder)
    if filename:
        folder = os.path.join(folder, filename)

    files = glob.glob(folder)
    if len(files) == 1:
        return files[0]
    else:
        return files


def get_file(folder, *args):
    folder = _get_folder_path(folder)
    filename = os.path.join(folder, *args)
    if not os.path.isfile(filename):
        raise OSError("Path '%s' not found." % filename)

    with open(filename, "r") as infile:
        ret = infile.read()

    return ret


def get_molecule(name, orient=True):
    """
    Returns a Molecule object from the available stored objects.
    """
    folder = _get_folder_path("molecules")

    return Molecule.from_file(os.path.join(folder, name), orient=orient)


def get_options(name):
    """
    Returns a default options dictionary
    """
    folder = _get_folder_path("options")
    if ".json" not in name:
        name += ".json"

    with open(os.path.join(folder, name), "r") as infile:
        ret = json.load(infile)
    return ret