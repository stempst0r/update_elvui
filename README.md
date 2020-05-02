# update_elvui

***Supports Retail and Classic WoW***

Updatescript for the World of Warcraft Interface Addon 'ElvUI' written in Python. 

Just get sure all dependencies are installed with the following command:

> pip install configparser, requests

In the configfile **settings.ini** set the **game directory** to the path of your World of Warcraft installation. For example

> C:/Program Files/World of Warcraft

(This is the standard path on Windows machines)

And choose if u want to update ElvUI for Retail or Classic WoW by writing "True" behind it in the config file:

> classic = True

> retail = True

(This will update both versions of ElvUI)


After config is done done just start the script with

> python update_elvui.py

If 'Elvui' is not installed on your machine or is not up2date, the latest version will be pulled and unzipped.
