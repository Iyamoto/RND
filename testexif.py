# How to wotk with EXIF?

import os
import fire
from PIL import Image
from PIL.ExifTags import TAGS

def getgpsmetadata(imagepath=''):
    """Returns EXIF GPS metadata"""
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
            exifgps = exifdata['GPSInfo']
            if exifgps:
                return exifgps
    except:
        return None
        # raise BaseException('Something went wrong')

if __name__ == '__main__':
    if os.environ.get('PYCHARM_HOSTED'):
        imagepath = os.path.join('images', 't2.jpg')
        getgpsmetadata(imagepath=imagepath)
    else:
        fire.Fire(getgpsmetadata())