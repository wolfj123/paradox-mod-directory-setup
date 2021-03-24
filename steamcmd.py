import os
import subprocess
import time
import shutil
import urllib.request
import re


def main():
    steamcmd_path = "E:\steamcmd"
    steamcmd_exe = os.path.join(steamcmd_path, "steamcmd.exe")
    login_command = "login anonymous"
    url = ""

    game_id , mod_id = collect_info_from_url("https://steamcommunity.com/sharedfiles/filedetails/?id=2428511640")
    download_command = "workshop_download_item {game_id} {mod_id}".format(game_id = game_id, mod_id = mod_id)
    download_dir = os.path.join(steamcmd_path, "steamapps", "workshop", "content", "{game_id}", "{mod_id}").format(game_id = game_id, mod_id = mod_id)
    download_mod(steamcmd_exe, login_command, download_command)
    move_downloaded_dir_to_cwd(download_dir, mod_id)

def collect_info_from_url(url):
    mod_id = re.findall('id=(\d+)', url)[0]
    f = urllib.request.urlopen(url)
    url_source = f.read().decode("utf-8")
    game_id = re.findall('\t<a href="https://steamcommunity.com/app/(\d+)', url_source)[0]
    return game_id, mod_id

def download_mod(steamcmd_exe, login_command, download_command):
    os.system("{steamcmd_exe} +{login_command} +{download_command} +quit".format(steamcmd_exe = steamcmd_exe, login_command = login_command, download_command = download_command))

def move_downloaded_dir_to_cwd(download_dir, mod_id):
    try:
        shutil.move(download_dir, os.path.join(os.getcwd(), mod_id))
    except:
        print("FAILED")

main()