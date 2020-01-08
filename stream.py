import os
import sys

team = sys.argv[1]
url = f"http://35.232.51.219/{team}.m3u8"
command = f"nohup mpv {url} >/dev/null 2>&1 &"

os.system(command)
