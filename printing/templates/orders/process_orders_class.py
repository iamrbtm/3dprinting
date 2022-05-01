from printing import db, gcode
from printing.models import *

class Ordering:
    def __init__(self, date_needed, project_name, qty, weight_in_g, time_to_print, setuptime, taredowntime, time, filused, c_labor, c_machine, c_materials, c_markup, shipping, userid, active_status, customerfk, order_status, machinefk, filamentfk, gcodefilename ):
        self.date_needed = date_needed
        self.project_name = project_name
        self.qty = qty
        self.weight_in_g = weight_in_g
        self.time_to_print = time_to_print
        self.setuptime = setuptime
        self.taredowntime = taredowntime
        self.time = time
        self.filused = filused
        self.c_labor = c_labor
        self.c_machine = c_machine
        self.c_materials = c_materials
        self.c_markup = c_markup
        self.shipping = shipping
        self.userid = userid
        self.active_status = active_status
        self.customerfk = customerfk
        self.order_status = order_status
        self.machinefk = machinefk
        self.filamentfk = filamentfk
        self.gcodefilename = gcodefilename
    
    def get_raw_data(self):
        # return filament used, time to print
        self.gcodefilename = gcode.save(file)
        with open ('printing/static/gcode/'+self.gcodefilename, 'r') as file:
            i = 0
            for line in file:
                if "used" in line:
                    self.filused = line.replace(";Filament used: ", "")
                elif "TIME" in line:
                    self.time = line.replace(";TIME:", "")
                i += 1
                if i >= 20:
                    break

        self.time_to_print = calculate_print_time(time)
        self.weight_in_g = calculate_weight(filused, filament)
        return [self.time_to_print, self.weight_in_g, self.filused, self.time]


    def calculate_print_time(self, ctime=self.time):
        timeinsec = int(self.time)

        day = timeinsec // (24 * 3600)

        timeinsec = timeinsec % (24 * 3600)
        hour = timeinsec // 3600

        timeinsec %= 3600
        minutes = timeinsec // 60

        timeinsec %= 60
        seconds = timeinsec

        if day == 0 and hour == 0:
            result = f"{minutes}m {seconds}s"
        elif day == 0 and hour > 0:
            result = f"{hour}h {minutes}m {seconds}s"
        elif day > 0:
            result = f"{day}d {hour}h {minutes}m {seconds}s"
        else:
            result = "failed"
        return result


    def calculate_weight(self):
        import math

        diameter = db.session.query(Filament.diameter).filter(Filament.id == self.filamentfk).scalar()
        density = db.session.query(Filament).filter(Filament.id==self.filamentfk).first().type_rel.densitygcm3
        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filused = float(self.weight_in_g.strip("\n").replace("m", ""))
        filcm = filused * 100
        radius = (diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * density
        weight = f"{round(weight)}g"
        return weight

    def calculate_cost(self):
        from string import digits
        #MATERIALS COSTING
        fil = db.session.query(Filament).filter(Filament.id == self.filamentfk).first()
        if  fil.diameter == 1.75:
            costPerMOfFil = fil.priceperroll / db.session.query(Filament).filter(Filament.id==self.filamentfk).first().type_rel.m_in_1kg_175
        else:
            costPerMOfFil = fil.priceperroll / db.session.query(Filament).filter(Filament.id==self.filamentfk).first().type_rel.m_in_1kg_3
        
        l_in_m = float(self.filused.strip().replace('m',''))
        self.c_materials = costPerMOfFil * l_in_m

        #MARKUP ON MATERIALS COSTING
        custmarkup = db.session.query(Customer.markuppercent).filter(Customer.id == self.customerfk).scalar()
        self.c_materials_markup = custmarkup * c_materials
        
        #LABOR COSTING
        totaltime = self.setuptime + self.taredowntime
        pricePerMin = db.session.query(Setup).first().pricePerHour / 60
        self.c_labor = pricePerMin * totaltime
        
        #MACHINE COSTING
        self.c_machine = 0
    
        return {'materials':self.c_materials, 'markup':self.c_materials_markup, 'labor':self.c_labor, 'machine':self.c_machine}

    def calc_total_time(self):
        labortime = (self.setuptime + self.taredowntime) * 60
        labortime = labortime + self.time 
        return calculate_print_time(labortime)