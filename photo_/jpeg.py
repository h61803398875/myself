# -*- coding:utf8 -*-


from exceptions import IOError

import PIL.ImageFile
import PIL.Image

img = PIL.Image.open("F:/puple.PNG")

# src_file_name = "F:/puple.PNG.11.jpg"
# dest_file_name = "F:/puple.PNG.2.jpg"

for i in xrange(80):

    # img = PIL.Image.open(src_file_name)
    dest_file_name = "F:/compress/puple.PNG.{}.jpg".format(i)
    try:
        img.save(dest_file_name, "JPEG", quality=i+1, optimize=True, progressive=True)
    except IOError:
        print "failed {}".format(i)

    # src_file_name = dest_file_name
