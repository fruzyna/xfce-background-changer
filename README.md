# xfce-background-changer
A python script I built to either set a given, random, or filtered background for xfce

Examples:

python background.py set all random

-Sets all monitors to a different random image

python background.py set all image.jpg

-Sets all monitors to the given image

python background.py set 0,2 random

-Sets monitors 0 and 2 to a different random image

python background.py set 1 f:filter

-Sets monitor 1 to a random image containing the phrase "filter"

python background.py set 0,1,2 random image.jpg f:filter

-Sets monitor 0 to a random image, monitor 1 to image.jpg, and monitor 2 to a random image containing the phrase "filter"

python background.py list

-Lists all files in backgrounds directory

python background.py list filter

-Lists all files containing phrase "filter" in backgrounds directory

python save configName

-Saves current wallpapers to a file named configName.cfg

python load configName

-Loads current wallpapers from the file configName.cfg
