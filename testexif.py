# How to wotk with EXIF?

import os
import fire
from PIL import Image
from PIL.ExifTags import TAGS

def getexif(imagepath=''):
    """Returns EXIF metadata"""
    exifdata = dict()
    if not os.path.isfile(imagepath):
        raise FileExistsError('"' + imagepath + '" is not file')
    imgFile = Image.open(imagepath)
    try:
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifdata[decoded] = value
            return exifdata
    except:
        raise BaseException('Something went wrong')

def getgps(imagepath=''):
    """Returns EXIF GPS metadata"""
    exifdata = getexif(imagepath=imagepath)
    try:
        exifgps = exifdata['GPSInfo']
        return exifgps
    except:
        raise BaseException('Something went wrong')

if __name__ == '__main__':
    if os.environ.get('PYCHARM_HOSTED'):
        imagepath = os.path.join('images', 't6.jpg')
        try:
            exif = getexif(imagepath=imagepath)
            print(exif)
            gps = getgps(imagepath=imagepath)
            print(gps)
        except:
            pass
    else:
        fire.Fire(getgps())