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

args = sys.argv.copy()
args.pop(0)
default_target_dir = os.getcwd()


def main():
    steamcmd_path = "E:\steamcmd"
    steamcmd_exe = os.path.join(steamcmd_path, "steamcmd.exe")
    login_command = "login anonymous"
    list_of_created_dirs = []

    for url in args:
        game_id , mod_id = collect_info_from_url(url)
        download_command = "workshop_download_item {game_id} {mod_id}".format(game_id = game_id, mod_id = mod_id)
        download_dir = os.path.join(steamcmd_path, "steamapps", "workshop", "content", "{game_id}", "{mod_id}").format(game_id = game_id, mod_id = mod_id)
        download_mod(steamcmd_exe, login_command, download_command)
        new_dir = move_downloaded_dir_to_target_dir(download_dir, default_target_dir, mod_id)
        if new_dir:
            list_of_created_dirs.append(new_dir)

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