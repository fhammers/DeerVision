from PIL import Image, ExifTags
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()
root.withdraw()

#Ask user for file
picURL = askopenfilename()
root.destroy()

img = Image.open(picURL)
img_exif = img.getexif()

if img_exif is None:
    print("Sorry, image has no exif data.")

else:
    img_exif_dict = dict(img_exif)
    #print(img_exif_dict, end='\n')

    for key, val in img_exif_dict.items():
        if ExifTags.TAGS[key] == "GPSInfo":
            print(f"{ExifTags.TAGS[key]}:{repr(val)}")