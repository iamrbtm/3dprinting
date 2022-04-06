from PIL import Image
from flask import url_for
from printing import photos, db
from printing.models import *
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
        

def calculate_roi_per_min(machine, years_for_roi, printing_hours_per_year):
    mins = ((printing_hours_per_year * 60) * 52) * years_for_roi #Convert Years to min
    cost = db.session.query(Machine.purchase_price).filter(Machine.name == machine).scalar() # get cost of machine
    roipermin = cost / mins   #cost / mins = roi per min
    return roipermin

