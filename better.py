import os, sys
os.system('nohup mpv http://35.232.51.219/' + sys.argv[1] + '.m3u8 >/dev/null 2>&1 &')