# Requires:
#
# pip: pyvirtualdisplay, selenium, beautifulsoup4
# packages: geckodriver, firefox

import os
import sys
import time
import webbrowser

from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

display = Display(visible=0, size=(1800, 1000))
display.start()

url = "https://sportsurge.net/#/events/19"

driver = webdriver.Firefox()

driver.get(url)
timeout = 20
try:
    element_present = EC.presence_of_element_located(
        (By.CLASS_NAME, "card-action-text")
    )
    WebDriverWait(driver, timeout).until(element_present)

    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    lines = str(soup).splitlines()

    for line in lines:
        if sys.argv[1].lower() in line.lower():
            streamline = line.lower()
            streamlist = (
                "https://sportsurge.net/#/streamlist/"
                + streamline[
                    streamline.find("#/methods/")
                    + 10 : streamline.find("#/methods/")
                    + 14
                ]
            )

    driver.get(streamlist)
    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "stream-row"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

except TimeoutException:
    print(
        "Timed out waiting for page to load. This may occur when only one game is currently being played. Trying to continue..."
    )
    driver.get(url)
    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "stream-row"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

html = driver.page_source
soup = BeautifulSoup(html, features="lxml")

soupstr = str(soup).replace("</tbody>", "<tr")
lines = soupstr.split("<tr")

streaminfos = []
streamurls = []

for line in lines:
    if (("720p" in line) or ("1080p" in line)) and (
        ("<td>0</td>" in line) or ("<td>1</td>")
    ):
        streaminfos.append(line)

for streaminfo in streaminfos:
    streamurls.append(
        streaminfo[streaminfo.find('<a href="') + 9 : streaminfo.find('target="') - 2]
    )

display.stop()

print("\nOpening top available stream...")

streamopen = False
for s in streamurls:
    if "buffstreamz.com" in s:
        os.system("xdg-open " + s + " &> /dev/null")
        streamopen = True
    elif "ripple.is" in s:
        os.system("xdg-open " + s + " &> /dev/null")
        streamopen = True
    elif "nbastreams.xyz" in s:
        for line in HTMLSession().get(s).text.split():
            if 'src="http://crackstreams.ga/nba/' in line:
                for pline in (
                    HTMLSession()
                    .get(line[line.find('src="http://crackstreams.ga/nba/') + 5 : -1])
                    .text.split()
                ):
                    if '"http://' in pline:
                        os.system("nohup mpv " + pline[1:-2] + "&> /dev/null")
                        exit()

if not streamopen:
    os.system("xdg-open " + streamurls[0] + " &> /dev/null")

if input("Does this stream work? (y/n): ").lower() == "n":
    with open("streams.txt", "w+") as f:
        for stream in streamurls:
            f.write(stream + "\n")
    print(
        "\nA list of available streams has been saved to 'streams.txt' in your current directory.\n"
    )
    try:
        os.system("nohup subl streams.txt &> /dev/null")
    except BaseException:
        pass
else:
    print()
