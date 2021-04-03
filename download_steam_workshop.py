# USAGE:
# python download_steam_workshop.py <workshop_url_1> <workshop_url_2> ... <workshop_url_n>
# 
# CONFIG:
# steamcmd_path : path to steamcmd parent directory
# target_dir : path to dir to move downloaded file to
#


import os
import subprocess
import time
import shutil
import urllib.request
import re
import sys
import json

args = sys.argv.copy()
args.pop(0)

default_target_dir = os.getcwd()
target_dir = ""

default_steamcmd_path = "E:\steamcmd"
steamcmd_path = ""
steamcmd_exe_name = "steamcmd.exe"

def main():
    get_config_settings()
    steamcmd_exe = os.path.join(steamcmd_path, steamcmd_exe_name)
    login_command = "login anonymous"
    list_of_created_dirs = []

    for url in args:
        game_id , mod_id = collect_info_from_url(url)
        download_command = "workshop_download_item {game_id} {mod_id}".format(game_id = game_id, mod_id = mod_id)
        download_dir = os.path.join(steamcmd_path, "steamapps", "workshop", "content", "{game_id}", "{mod_id}").format(game_id = game_id, mod_id = mod_id)
        download_mod(steamcmd_exe, login_command, download_command)
        new_dir = move_downloaded_dir_to_target_dir(download_dir, target_dir, mod_id)
        if new_dir:
            list_of_created_dirs.append(new_dir)

def get_config_settings():
    global steamcmd_path
    global target_dir
    config_file = os.path.join(os.getcwd(), "config.json")
    with open(config_file) as f:
        data = json.load(f)
        if('steamcmd_path' in data):
            steamcmd_path = data['steamcmd_path']
        else:
            steamcmd_path = default_steamcmd_path
        
        if('target_dir' in data):
            target_dir = data['target_dir']
        else:
            target_dir = default_target_dir


def collect_info_from_url(url):
    mod_id = re.findall('id=(\d+)', url)[0]
    f = urllib.request.urlopen(url)
    url_source = f.read().decode("utf-8")
    game_id = re.findall('\t<a href="https://steamcommunity.com/app/(\d+)', url_source)[0]
    return game_id, mod_id

def download_mod(steamcmd_exe, login_command, download_command):
    os.system("{steamcmd_exe} +{login_command} +{download_command} +quit".format(steamcmd_exe = steamcmd_exe, login_command = login_command, download_command = download_command))

def move_downloaded_dir_to_target_dir(download_dir, target_dir, mod_id):
    try:
        location = os.path.join(target_dir, mod_id)
        shutil.move(download_dir, os.path.join(target_dir, mod_id))
        return location
    except:
        print("FAILED")
        return ""


main()