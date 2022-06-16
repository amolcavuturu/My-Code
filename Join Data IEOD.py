import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, zipfile

#####extract zipfiles----------------------not useful directly import in amibroker
dir_name = 'C:\\path....'
extension = ".zip"

os.chdir(dir_name) # change directory from working dir to dir with files

for item in os.listdir(dir_name): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(dir_name) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file
        

import zipfile,fnmatch,os

rootPath = r"......."
pattern = '*.zip'
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        print(os.path.join(root, filename))
        zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))


  
# create a dictionary with file names as keys
# and for each file name the paths where they
# were found
file_paths = {}
for root, dirs, files in os.walk('......'):
    for f in files:
        if f.endswith('.txt'):
            if f not in file_paths:
                file_paths[f] = []
            file_paths[f].append(root)

print(file_paths)



# for each file in the dictionary, concatenate
# the content of the files in each directory
# and write the merged content into a file
# with the same name at the top directory
for f, paths in file_paths.items():
    txt = []
    for p in paths:
        with open(os.path.join(p, f)) as f2:
            txt.append(f2.read())
            print(txt)
    with open(f, 'w') as f3:
        print(f3)
        f3.write(''.join(txt))
        


mapped_files = {}

for path, subdirs, files in os.walk("......."):
    for file in files:
        if file.endswith(".txt"):
            if file in mapped_files:
                existing = mapped_files[file]
                mapped_files[file] = existing.append(path)
            else:
                mapped_files[file] = [path]

for key in mapped_files:
    files = mapped_files[key]
    first_f = os.path.join(path, files[0])
    with open(first_f, "a+") as current_file: 
        for path in files[1:]: # start at the second index
            f = os.path.join(path, key)
            content = open(f,"r").read()
            current_file.write(content)


























