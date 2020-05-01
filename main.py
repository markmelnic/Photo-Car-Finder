
import os
from selen_module import *


if __name__ == '__main__':
    maindir = os.getcwd()
    
    with os.scandir("./photos") as entries:
        os.chdir("./photos")
        photos = []
        for entry in entries:
            if entry.is_file():
                print(entry)
                photos.append(entry.name)
    os.chdir(maindir)
    
    instances = []
    for photo in photos:
        dv = boot()
        titles = finder(dv, photo)
        print(titles)
        print("One of these is the car in the photo.")
        killd(dv)
