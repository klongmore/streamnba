from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import os, sys, time

display = Display(visible=0, size=(800, 600))
display.start()

url = "https://sportsurge.net/#/events/19"

driver = webdriver.Firefox() 

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, features="lxml")

lines = str(soup).splitlines()

for line in lines:
	if sys.argv[1].lower() in line.lower():
		streamlist = "https://sportsurge.net/#/streamlist/" + line[line.find('#/methods/') + 10:line.find('text" href="') + 14]

driver.get(streamlist)

html = driver.page_source
soup = BeautifulSoup(html, features="lxml")

soupstr = str(soup).replace('</tbody>', '<tr')
lines = soupstr.split('<tr')

streaminfos = []
streamurls = []

for line in lines:
	if (("720p" in line) or ("1080p" in line)) and (("<td>0</td>" in line) or ("<td>1</td>")):
		streaminfos.append(line)

for streaminfo in streaminfos:
	streamurls.append(streaminfo[streaminfo.find('<a href="') + 9:streaminfo.find('target="') - 2])

display.stop()

print("\nOpening top available stream...")
os.system('xdg-open ' + streamurls[0])

if input('Does this stream work? (y/n): ').lower() == 'n':
	with open('streams.txt', 'w+') as f:
		for stream in streamurls:
			f.write(stream + "\n")
	print("\nOpening list of other available streams...\n")
	os.system('nohup subl streams.txt &> /dev/null')
else:
	print("\n")