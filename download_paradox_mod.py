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
    zip_url = ''
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver_path, options = options)  # Optional argument, if not specified will search path.
    driver.get(mod_url)
    time.sleep(5) # Let the user actually see something!
    url_source = driver.page_source

    print("********************* INFO *********************************")
    # info = re.findall('url\("https://modscontent.paradox-interactive.com/([\d|[a-zA-Z]]+)/([\d|[a-zA-Z]|\-]+)', url_source)
    info = re.findall('https://modscontent.paradox-interactive.com/([\d|[a-zA-Z]]+)/', url_source)
    print(info)

    # game_code = info[0]
    # mod_code = info[1]
    # mod_latest_version = re.findall('src-components-Mods-Details-Header-styles__value--2VrqZ">(\d+)<', url_source)[0]
 
    driver.quit()

    
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