import sys
import shutil
import os
import ntpath
import posixpath
import re
import argparse

backup_folder = "BACKUP"

# Create the parser
my_parser = argparse.ArgumentParser(description='Setup Paradox-Interactive mods for use in GOG versions of the game.')


# Add the arguments
my_parser.add_argument('-dirs',
                       type=str,
                       metavar="dirs",
                       help='mod directory(ies)', nargs="+")

args = my_parser.parse_args()

if not args.dirs:
    print('Must specify mod directories')
    quit()

def main():
    for dr in args.dirs:
        path , dir_name = ntpath.split(dr)
        handle_mod_dir(path, dir_name)


#https://docs.python.org/2/howto/regex.html
def handle_mod_dir(path, mod_dir):
    full_mode_dir_path = os.path.join(path, mod_dir)
    mod_name_pattern = re.compile('^name="(.*)"$')
    mod_name = ""

    # GET MODE NAME FROM DESCRIPTOR FILE
    descriptor_file = os.path.join(full_mode_dir_path, "descriptor.mod")
    f = open(descriptor_file, "r")
    for i, line in enumerate(open(descriptor_file)):
        for match in re.finditer(mod_name_pattern, line):
            mod_name = match.group(1)
            break
    f.close()

    # RENAME DIR AND COPY DESCRIPTOR FILE
    upper_descriptor_file = os.path.join(path, mod_name + ".mod")
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


def backup_dir(dr):
    backup_dir = os.path.join(dr, backup_folder)
    try:
        os.mkdir(backup_dir)
    except OSError:
        print ("Creation of the directory %s failed" % backup_dir)
        quit()
    else:
        file_names = os.listdir(dr)
        file_names.remove(backup_folder)

        for file_name in file_names:
            shutil.move(os.path.join(dr, file_name), backup_dir)
            

main()