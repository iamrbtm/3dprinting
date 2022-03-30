from PIL import Image
from flask import url_for
from printing import photos, db
import os

def resize_images(fn, name):
    with Image.open('printing/static/images/'+fn) as im:
        
        name = name.replace(" ","_").lower()
        ext = os.path.splitext(fn)
        
        #main photo
        largephoto = im.resize((500,500))
        largephoto.save('printing/static/images/'+name+"_500x500"+ext[1])

        #thumbnail photo
        smallphoto = im.resize((64,64))
        smallphoto.save('printing/static/images/'+name+"_64x64"+ext[1])
        
        thumb = str(name+"_64x64"+ext[1])
        lg = str(name+"_500x500"+ext[1])
        
        os.remove('printing/static/images/'+fn)
    return {'thumb':thumb, 'large':lg}
        
    