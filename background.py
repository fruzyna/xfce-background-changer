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
        file = random.choice(getFilteredFiles(file.split(":")[1].split(",")))
    elif file == "random":
        file = random.choice(files)
    changeWallpaper(monitor, image, file)
    return;

def getFilteredFiles(filters):
    options = []
    for filter in filters:
        options += [f for f in files if filter in f]
    return options

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
elif command == "list":
    if len(sys.argv) > 2:
        filters = [sys.argv[i] for i in range(2, len(sys.argv))] 
        print("Files under " + ''.join(filters) + " in " + path)
        for f in getFilteredFiles(filters):
            print(f)
    else:
        print("Files in " + path)
        for f in files:
            print(f)
else:
    print("Unknown Command")
    help()
