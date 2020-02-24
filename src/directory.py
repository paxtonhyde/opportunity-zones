import os
this_directory = os.path.realpath(".")
home = os.path.split(this_directory)[0]
data = os.path.join(home, "data")
images = os.path.join(home, "images")