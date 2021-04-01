import os
import subprocess
import time
import shutil
import urllib.request
import re
import sys

from selenium import webdriver

chromedriver_path = r"C:\Users\user\Documents\My Documents\Tools\chromedriver\chromedriver_89.exe"
# chromedriver_path = "C:\\Users\\user\\Documents\\My Documents\\Tools\\chromedriver\\chromedriver.exe"
steamcmd_path = "E:\steamcmd"

args = sys.argv.copy()
args.pop(0)

def main():
    for url in args:
        zip_url = get_mod_download_url(url)
        print(zip_url)
        # download_mod(zip_url)
        # move_downloaded_dir_to_cwd()

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
    print(zip_url)
    return zip_url

def download_mod(zip_url):
    print("TODO")

def move_downloaded_dir_to_cwd(download_dir, mod_id):
    print("TODO")


def chromedirver_example():
    driver = webdriver.Chrome(chromedriver_path)  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/')
    time.sleep(5) # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5) # Let the user actually see something!
    driver.quit()

main()