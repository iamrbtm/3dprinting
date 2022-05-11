from printing import db
from printing.models import *

class Gcode:
    def __init__(self, gcodefile, filamentfk):
        self.filamentfk = filamentfk
        self.gcodefile = gcodefile

        with open ('printing/static/uploads/'+self.gcodefile, 'r') as file:
            i = 0
            for line in file:
                if "used" in line:
                    filused = line.replace(";Filament used: ", "")
                elif "TIME" in line:
                    time = line.replace(";TIME:", "")
                i += 1
                if i >= 40: #only 40 lines of the file are read
                    break
        self.filused = filused 
        self.time = time
    
    def get_length_used(self):
        pass
    
    