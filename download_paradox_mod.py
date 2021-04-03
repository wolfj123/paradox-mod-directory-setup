# USAGE:
# python download_paradox_mod.py <paradox_url_1> <paradox_url_2> ... <paradox_url_n>
# 
# CONFIG:
# chromedriver_path = path to chromedriver parent directory
# target_dir : path to dir to move downloaded file to
#


import os
import subprocess
import time
import shutil
import urllib.request
import re
import sys
import zipfile
import json
from selenium import webdriver


args = sys.argv.copy()
args.pop(0)

download_file_name = 'download.zip'
new_mod_dir = 'NEW_MOD'

default_chromedriver_path = r"C:\Users\user\Documents\My Documents\Tools\chromedriver\chromedriver_89.exe"
chromedriver_path = ""

default_target_dir = os.getcwd()
target_dir = ""


def main():
    get_config_settings()
    list_of_created_dirs = []
    for url in args:
        zip_url = get_mod_download_url(url)
        download_zip_file(zip_url)
        extract_from_zip_file(os.getcwd(), download_file_name)
        new_dir = move_downloaded_dir_to_target_dir(os.path.join(os.getcwd(), new_mod_dir), target_dir, new_mod_dir)
        if new_dir:
            list_of_created_dirs.append(new_dir)


def get_config_settings():
    global chromedriver_path
    global target_dir
    config_file = os.path.join(os.getcwd(), "config.json")
    with open(config_file) as f:
        data = json.load(f)
        if('chromedriver_path' in data):
            chromedriver_path = data['chromedriver_path']
        else:
            chromedriver_path = default_chromedriver_path
        
        if('target_dir' in data):
            target_dir = data['target_dir']
        else:
            target_dir = default_target_dir


def get_mod_download_url(mod_url):
    zip_url = 'https://modscontent.paradox-interactive.com/{game_code}/{mod_code}/repo/Any__Any/{mod_version}/complete/{mod_code}.zip'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver_path, options = options)  # Optional argument, if not specified will search path.
    driver.get(mod_url)
    time.sleep(3) # Let the user actually see something!
    url_source = driver.page_source
    info = re.findall('https://modscontent.paradox-interactive.com/([a-zA-Z|\d]+)/([\-|a-zA-Z|\d]+)', url_source)
    mod_latest_version = re.findall('src-components-Mods-Details-Header-styles__value--2VrqZ">(\d+)<', url_source)[0]
    game_code = info[0][0]
    mod_code = info[0][1]
    driver.quit()
    zip_url = zip_url.format(game_code = game_code, mod_code = mod_code, mod_version = mod_latest_version)
    return zip_url

def download_zip_file(zip_url):
    remote = urllib.request.urlopen(zip_url)  # read remote file
    data = remote.read()  # read from remote file
    remote.close()  # close urllib request
    local = open(download_file_name, 'wb')  # write binary to local file
    local.write(data)
    local.close()  # close file

def extract_from_zip_file(path, name):
    zip_file = os.path.join(path, name)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        os.mkdir(os.path.join(new_mod_dir))
        zip_ref.extractall(new_mod_dir)
    os.remove(zip_file)
    
def move_downloaded_dir_to_target_dir(download_dir, target_dir, mod_name):
    try:
        location = os.path.join(target_dir, mod_name)
        print(location)
        shutil.move(download_dir, location)
        return location
    except:
        print("FAILED")
        return ""


main()