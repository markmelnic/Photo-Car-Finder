
import os
from selen_module import *


if __name__ == '__main__':
    with os.scandir("./photos") as entries:
        photos = []
        for entry in entries:
            if entry.is_file():
                print(entry)
                photos.append(entry.name)

    for photo in photos:
        dv = boot()
        titles = finder(dv, photo)
        print(titles)
        print("One of these is the car in the photo.")
        killd(dv)

        boot_u(titles[0])
