import os
import subprocess
import time
import shutil


def main():
    steamcmd_path = "E:\steamcmd"
    steamcmd_exe = os.path.join(steamcmd_path, "steamcmd.exe")
    login_command = "login anonymous"
    download_command = "workshop_download_item {game_id} {mod_id}" 
    download_dir = os.path.join(steamcmd_path, "steamapps", "workshop", "content", "{game_id}", "{mod_id}") 
    url = ""
    # game_id , mod_id = collect_info_from_url(url)
    # download_command = download_command.format(game_id = game_id, mod_id = mod_id)
    # download_dir = download_dir.format(game_id = game_id, mod_id = mod_id)
    download_command = download_command.format(game_id = "281990", mod_id = "1610578060")
    download_dir = download_dir.format(game_id = "281990", mod_id = "1610578060")
    download_mod(steamcmd_exe, login_command, download_command)
    move_downloaded_dir_to_cwd(download_dir, "1610578060")

def collect_info_from_url(url):
    print("TODO")

def download_mod(steamcmd_exe, login_command, download_command):
    os.system("{steamcmd_exe} +{login_command} +{download_command} +quit".format(steamcmd_exe = steamcmd_exe, login_command = login_command, download_command = download_command))

def move_downloaded_dir_to_cwd(download_dir, mod_id):
    print(os.getcwd())
    shutil.move(download_dir, os.path.join(os.getcwd(), mod_id))


main()