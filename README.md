# xfce-background-changer
A python script I built to either set a given, random, or filtered background for xfce

Examples:

background.sh set all random

-Sets all monitors to a different random image

background.sh set all image.jpg

-Sets all monitors to the given image

background.sh set 0,2 random

-Sets monitors 0 and 2 to a different random image

background.sh set 1 f:filter

-Sets monitor 1 to a random image containing the phrase "filter"

background.sh set 0,1,2 random image.jpg f:filter

-Sets monitor 0 to a random image, monitor 1 to image.jpg, and monitor 2 to a random image containing the phrase "filter"

background.sh list

-Lists all files in backgrounds directory

background.sh list filter

-Lists all files containing phrase "filter" in backgrounds directory

background.sh save configName

-Saves current wallpapers to a file named configName.cfg

background.sh load configName

-Loads current wallpapers from the file configName.cfg

backgorund.sh config

-Prints out current configuration

background.sh rebuild

-Helps the user build a new config file
