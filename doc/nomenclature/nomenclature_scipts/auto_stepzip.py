from os.path import basename, splitext
import zipfile

from convert_nomenclature import list_files_sorted, root

filenames = list_files_sorted(root)
assert len(filenames) % 2 == 0
filenames_coupled = [filenames[n:n+2] for n in range(0, len(filenames), 2)]

for file_a, file_b in filenames_coupled:
    assert splitext(file_a)[0] == splitext(file_b)[0]
    print(file_a)
    print(file_b)
    print()
    zf = zipfile.ZipFile('%s.stepzip' % splitext(file_a)[0],
                         'w',
                         zipfile.ZIP_DEFLATED)
    zf.write(file_a, basename(file_a))
    zf.write(file_b, basename(file_b))
    zf.close()
