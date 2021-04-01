import os
import subprocess
import time
import shutil
import urllib.request
import re
import sys

from selenium import webdriver  


args = sys.argv.copy()
args.pop(0)


def main():
    for url in args:
        zip_url = get_mod_download_url(url)
        print(zip_url)
        # download_mod(zip_url)
        # move_downloaded_dir_to_cwd()

def get_mod_download_url(mod_url):
    driver = webdriver.Chrome()
    zip_url = ''
    driver.get(mod_url)
    # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"ptifrmtgtframe")))
    # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='HRS_APPL_WRK_HRS_PAGE_TITLE']")))
    time.sleep(4)
    print (driver.page_source.encode('utf-8')) 
    
    # f = urllib.request.urlopen(mod_url)
    # url_source = f.read().decode("utf-8")
    # print(url_source)
    # # info = re.findall('url\("https://modscontent.paradox-interactive.com/([\d|[a-zA-Z]]+)/([\d|[a-zA-Z]|\-]+)', url_source)
    # info = re.findall('"https://modscontent.paradox-interactive.com/([\d|[a-zA-Z]]+)/', url_source)
    # print(info)

    # game_code = info[0]
    # mod_code = info[1]
    # mod_latest_version = re.findall('src-components-Mods-Details-Header-styles__value--2VrqZ">(\d+)<', url_source)[0]

    return zip_url

def download_mod(zip_url):
    print("TODO")

def move_downloaded_dir_to_cwd(download_dir, mod_id):
    print("TODO")

main()