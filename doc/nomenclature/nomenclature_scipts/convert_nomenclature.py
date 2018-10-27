from os import walk, rename, remove
from os.path import join, dirname, basename, splitext

root = "/home/guillaume/_Repositories/github/osv-team/osvcad/sample_projects/car/shelf"


def list_files_sorted(folder):

    filenames = []

    for path, subdirs, files in walk(root):
        for name in files:
            filenames.append(join(path, name))

    return sorted(filenames)

if __name__ == "__main__":

    for name in list_files_sorted(root):
        if splitext(name)[1].lower() == ".stepzip":
            remove(name)
        else:
            dir_ = dirname(name)
            file_ = basename(name)
            new_file_ = file_.replace("_", "-").replace("#", "_")
            new_name = join(dir_, new_file_)
            rename(name, new_name)
