import shutil
import os


path = ".\\Logs"
directories = [x[0] for x in os.walk(path) if x[0] != path]
[shutil.rmtree(x) for x in directories]
