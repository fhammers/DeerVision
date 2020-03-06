from PIL import Image, ExifTags

img = Image.open(r'C:\Users\Michael\OneDrive\Juniata\Advanced Lab\Thermal Content\Patuxent River Park MD 02 19 2020\100MEDIA\DJI_0233R.JPG')
img_exif = img.getexif()
#print(type(img_exif))
# <class 'PIL.Image.Exif'>

if img_exif is None:
    print("Sorry, image has no exif data.")

else:
    img_exif_dict = dict(img_exif)
    #print(img_exif_dict)
    # { ... 42035: 'FUJIFILM', 42036: 'XF23mmF2 R WR', 42037: '75A14188' ... }
    for key, val in img_exif_dict.items():
        if key in ExifTags.TAGS:
            print(f"{ExifTags.TAGS[key]}:{repr(val)}")

    gpsinfo = {}

    for key in img_exif['GPSInfo'].keys():
        decode = ExifTags.GPSTAGS.get(key,key)
        gpsinfo[decode] = img_exif_dict['GPSInfo'][key]

    print (gpsinfo)