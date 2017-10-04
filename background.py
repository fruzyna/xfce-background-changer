import subprocess
import random
import sys
from os import listdir
from os.path import isdir, isfile, join, splitext

#definitions
path = "."
files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == ".jpg"]
image = "last-image"
monitorCount = 0
resolutions = ""

#loads in settings from file
def loadFromFile(fileName):
    global monitorCount
    global resolutions
    global files
    global path
    if isfile(fileName):
        file = open(fileName, 'r')
        settings = file.read().split('\n')
        for setting in settings:
            parts = setting.split(":")
            if parts[0] == "monitorCount":
                monitorCount = int(parts[1])
            elif parts[0] == "resolutions":
                resolutions = parts[1]
            elif parts[0] == "dir":
                path = parts[1]
                files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == ".jpg"]
    else:
        print("No config file!")
        buildConfigFile()
        main()
    return

#helps the user produce a config file
def buildConfigFile():
    monitorCount = promptMonitorCount()
    resolutions = promptScreenResolutions(monitorCount)
    path = promptBackgroundDir()
    
    file = open("background.cfg", 'w')
    file.write("dir:" + path + "\nmonitorCount:" + str(monitorCount) + "\nresolutions:" + resolutions)
    file.close()
    print("Config written to background.cfg")
    return

def promptMonitorCount():
    monitorCount = int(raw_input("How many displays do you have? "))
    if monitorCount <= 0:
        print("You must have at least 1 monitor!")
        monitorCount = promptMonitorCount()
    return monitorCount

def promptScreenResolutions(monitorCount):
    resolutions = ""
    for i in range(0, monitorCount):
        resolutions += promptScreenRes(i + 1)
    return resolutions

def promptScreenRes(screen):
    res = raw_input("Monitor " + str(screen) + " resolution ([Width]x[Height])? ")
    if 'x' in res:
        if screen != 1:
            res = "," + res
    else:
        print("Invalid input! Separate width and height with a 'x'")
        res = promptScreenRes(screen)
    return res

def promptBackgroundDir():
    path = raw_input("Where are your backgrounds stored? ")
    if not isdir(path):
        print("Not a valid directory!")
        path = promptBackgroundDir()
    return path

#runs the command to change the wallpaper according the the given criteria
def changeWallpaper(screen, type, file):
    print("Setting " + screen + " to " + file)
    bashCommand = "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor" + screen + "/workspace0/" + type + " -s " + path + "/" + file 
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return

#converts an entered string to a list of monitor numbers
def getMonitorList(screens):
    if screens == "all":
        monitors = [None] * monitorCount
        for i in range(0, monitorCount):
            monitors[i] = str(i)
        return monitors
    else:
        return screens.split(",")

#processes given file to pass on to monitor
def setMonitor(monitor, file):
    if file.startswith("f:"):
        file = randomWPrint(getFilteredFiles(file.split(":")[1].split(",")))
    elif file == "random":
        file = randomWPrint(files)
    changeWallpaper(monitor, image, file)
    return

#randomly chooses a file from a list then prints its name
def randomWPrint(files):
    file = random.choice(files)
    return file

#finds all files that are valid under the given filters
def getFilteredFiles(filters):
    options = []
    for filter in filters:
        options += [f for f in files if filter in f]
    return options

#saves the current wallpaper set to file
def saveConfig(configName):
    file = open(path + "/" + configName + ".cfg", 'w')
    for i in range(0, monitorCount):
        if i != 0:
            file.write(",")
        bashCommand = "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor" + str(i) + "/workspace0/" + image
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.rsplit('/', 1)[1]
        output = output.replace("\n", "");
        file.write(output);
    file.close()
    return

#loads a previously saved wallpaper set from file
def loadConfig(configName):
    location = path + "/" + configName + ".cfg"
    if isfile(location):
        file = open(location, 'r')
        backgrounds = file.read().split(",")
        for i in range(0, len(backgrounds)):
            changeWallpaper(str(i), image, backgrounds[i])
        file.close()
    else:
        print("The provided config does not exist!")
    return

#prints out a help dialog briefly explaining all commands
def help():
    print("Usage:")
    print("Commands:")
    print("set [monitors] [images]")
    print("list (filters)")
    print("save [config name]")
    print("load [config name]")
    print("config")
    print("rebuild")
    print("Options:")
    print("[monitors]\tall or comma separated list")
    print("[images]\tfile name in given directory, random, or a filter defined by f:[filter]")
    print("(filters)\toptional list of filters to sort with")
    print("[config name]\ta string for the config file name")
    return

#start actual script
def main():
    loadFromFile("./background.cfg")

    length = len(sys.argv)

    #checks if there are any command arguments
    if length == 1:
        help()
        sys.exit(0)

    command = sys.argv[1]

    #responds to the given command
    if command == "set":
        i = 3 
        monitors = getMonitorList(sys.argv[2])
        for monitor in monitors:
            if length - 3 >= len(monitors):
                setMonitor(monitor, sys.argv[i])
                i = i + 1
            else:
                setMonitor(monitor, sys.argv[3])
    elif command == "help":
        help()
    elif command == "list":
        if length > 2:
            filters = [sys.argv[i] for i in range(2, length)] 
            print("Files under " + ''.join(filters) + " in " + path)
            for f in getFilteredFiles(filters):
                print(f)
        else:
            print("Files in " + path)
            for f in files:
                print(f)
    elif command == "save":
        if length > 2:
            saveConfig(sys.argv[2])
        else:
            print("A config name must be provided!");
    elif command == "load":
        if length > 2:
            loadConfig(sys.argv[2])
        else:
            print("A config name must be provided!");
    elif command == "config":
        print("Config info: " + str(monitorCount) + ":" + resolutions)
        print("Background location: " + path)
    elif command == "rebuild":
        buildConfigFile()
    else:
        print("Unknown Command")
        help()
    return
	
main()
