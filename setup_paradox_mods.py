

import sys
import shutil
import os
import ntpath
import posixpath
import re

# import argparse

source_dir = ""
target_dir = ""
backup_folder = "BACKUP"
multiple_dir_mode = len(sys.argv) > 2
if multiple_dir_mode:
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
else:
    target_dir , source_dir = ntpath.split(sys.argv[1])


def main():
    if multiple_dir_mode:
        backup_target()
        copy_from_source()
        for root, dirs, filenames in os.walk(target_dir):
            for mod_dr in dirs:
                if (mod_dr != backup_folder):
                    handle_mod_dir(target_dir, mod_dr)
            break   #prevent descending into subfolders
    else:
        handle_mod_dir(target_dir, source_dir)


#https://docs.python.org/2/howto/regex.html
def handle_mod_dir(path, mod_dir):
    print(path)
    print(mod_dir)
    full_mode_dir_path = os.path.join(path, mod_dir)
    mod_name_pattern = re.compile('^name="(.*)"$')
    mod_name = ""

    # GET MODE NAME FROM DESCRIPTOR FILE
    descriptor_file = os.path.join(full_mode_dir_path, "descriptor.mod")
    f = open(descriptor_file, "r")
    for i, line in enumerate(open(descriptor_file)):
        for match in re.finditer(mod_name_pattern, line):
            # print('Found on line %s: %s' % (i+1, match.group(1)))
            mod_name = match.group(1)
            break
    f.close()

    # RENAME DIR AND COPY DESCRIPTOR FILE
    upper_descriptor_file = os.path.join(target_dir, mod_name + ".mod")
    if(mod_name != ""):
        shutil.copy(descriptor_file, upper_descriptor_file)
        os.rename(full_mode_dir_path, os.path.join(path, mod_name))

    # ADD CORRECT PATH TO UPPER DESCRIPTOR FILE
    mod_path_text = '"' + os.path.join(path, mod_name).replace(os.sep, posixpath.sep) + '"'
    mod_path_text_prefix = "path="
    with open(upper_descriptor_file, "r") as f:
        lines = f.readlines()
    with open(upper_descriptor_file, "w") as f:
        for line in lines:
            if not re.match('^path=".*"$', line): 
                f.write(line)
    with open(upper_descriptor_file, "a") as f:
        f.write(os.linesep)
        f.write(mod_path_text_prefix + mod_path_text)


def backup_target():
    backup_dir = os.path.join(target_dir, backup_folder)
    try:
        os.mkdir(backup_dir)
    except OSError:
        print ("Creation of the directory %s failed" % backup_dir)
        quit()
    else:
        # print ("Successfully created the directory %s " % backup_dir)
        file_names = os.listdir(target_dir)
        file_names.remove(backup_folder)

        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), backup_dir)
            


# TODO: first copy from source to target, then iterate target and modify
def copy_from_source():
    print("TODO")
    
    # file_names = os.listdir(target_dir +"\\"+"BACKUP")
    # print(target_dir)

    # for file_name in file_names:
    #     shutil.copy2(target_dir +"\\"+"BACKUP"+"\\"+file_name, target_dir)

main()