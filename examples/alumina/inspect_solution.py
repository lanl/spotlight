#! /usr/bin/env python

from klepto import archives

input_file = "tmp_spotlight/solution_alumina.pkl"
arch = archives.file_archive(input_file)
arch.load()

keys = arch.keys()
print(keys)
for key in keys:
    print(key, arch[key])

#from spotlight import archive
#archive_file = "tmp_spotlight/solution_alumina.pkl"
#arch = archive.Arch.read_data(solution_file)
