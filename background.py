import subprocess
import random
import sys
from os import listdir
from os.path import isfile, join

path = "/home/mail929/Dropbox/Walls"
files = [f for f in listdir(path) if isfile(join(path, f))]
image = "last-image"
monitorCount = 3

def changeWallpaper(screen, type, files):
    bashCommand = "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor" + screen + "/workspace0/" + type + " -s " + path + "/" + files 
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return;

def getMonitorList(screens):
    if screens == "all":
        monitors = [None] * monitorCount
        for i in range(0, monitorCount):
            monitors[i] = str(i)
        return monitors
    else:
        return screens.split(",")

def setMonitor(monitor, file):
    if file.startswith("f:"):
        options = []
        for filter in file.split(":")[1].split(","):
            options += [f for f in files if filter in f]
        file = random.choice(options)
    elif file == "random":
        file = random.choice(files)
    changeWallpaper(monitor, image, file)
    return;

def help():
    print("Usage:")
    print("Commands:");
    print("set [monitors] [images]");
    print("Options:");
    print("[monitors]\tall or comma separated list")
    print("[images]\tfile name in given directory, random, or a filter defined by f:[filter]");

if len(sys.argv) == 1:
    help()
    sys.exit(0)

command = sys.argv[1]
if command == "set":
    i = 3
    monitors = getMonitorList(sys.argv[2])
    for monitor in monitors:
        if len(sys.argv) - 3 >= len(monitors):
            setMonitor(monitor, sys.argv[i])
            i = i + 1
        else:
            setMonitor(monitor, sys.argv[3])
elif command == "help":
    help()
else:
    print("Unknown Command")
    help()
