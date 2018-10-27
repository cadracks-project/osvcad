from os import walk, rename, remove
from os.path import join, dirname, basename, splitext

from convert_nomenclature import list_files_sorted, root

for name in list_files_sorted(root):
    if splitext(name)[1].lower() == ".stepzip":
        remove(name)
