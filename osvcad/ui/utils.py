from os.path import isdir

def get_file_extension(filename):
    """Return the file extension, including the point (.)

    Parameters
    ----------
    filename : str
        The name of the file which extension we are interested in.
        It can be a standalone file name or a path to the file.

    """
    if not isdir(filename):  # check if directory
        index = filename.rfind('.')  # search for the last period
        if index > -1:
            return filename[index:].strip().lower()
        return ''
    else:
        return 'directory'
