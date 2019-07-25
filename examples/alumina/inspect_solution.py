#! /usr/bin/env python

import numpy
from klepto import archives

input_file = "tmp_spotlight/solution_alumina.pkl"
arch = archives.file_archive(input_file)
arch.load()

keys = arch.keys()
print(keys)
for key in keys:
    if key == "names":
        continue
    sol = arch[key]
    print("The key is", key)
    print("The shape of the parameters array is", numpy.array(sol[0]).shape)
    print("The shape of the solution array is", numpy.array(sol[1]).shape)
    print("The best parameters are:")
    for i, x in enumerate(sol[2]):
        print(arch["names"][i], x)
    print("The best cost function value is", sol[3])
    print()

#from spotlight import archive
#archive_file = "tmp_spotlight/solution_alumina.pkl"
#arch = archive.Arch.read_data(solution_file)
