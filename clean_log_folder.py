import os
from os import listdir
from os.path import isfile, join


path = ".\\Logs"
directories = [x[0] for x in os.walk(path) if x[0] != path]
files = [[ join(y,x) for x in listdir(y) if isfile(join(y,x))] for y in directories]
[[os.unlink(x) for x in y if ".gitignore" not in str(x)] for y in files]
