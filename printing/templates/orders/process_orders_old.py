from printing import db, gcodefile
from printing.models import *


def get_raw_data(filament, filename):
    # return filament used, time to print
    with open ('printing/static/uploads/'+filename, 'r') as file:
        i = 0
        for line in file:
            if "used" in line:
                filused = line.replace(";Filament used: ", "")
            elif "TIME" in line:
                time = line.replace(";TIME:", "")
            i += 1
            if i >= 20: #only 20 lines of the file are read
                break
        print(filused, time)

    formattedtime = calculate_print_time(time)
    formattedweight = calculate_weight(filused, filament)
    return [formattedtime, formattedweight, filused, time]


def calculate_print_time(timeinsec):
    timeinsec = int(timeinsec)

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


def calculate_weight(weightinm, filament):
    import math

    diameter = db.session.query(Filament.diameter).filter(Filament.id == filament).scalar()
    density = db.session.query(Filament).filter(Filament.id==filament).first().type_rel.densitygcm3
    # Volume = (length in m * 100) * pi() * ((diam/2)^2)
    filused = float(weightinm.strip("\n").replace("m", ""))
    filcm = filused * 100
    radius = (diameter / 2) / 10
    csarea = math.pi * (radius) ** 2
    volume = filcm * csarea
    weight = volume * density
    weight = f"{round(weight)}g"
    return weight

def calculate_cost(order, filused):
    from string import digits
    #MATERIALS COSTING
    fil = db.session.query(Filament).filter(Filament.id == order.filamentfk).first()
    if  fil.diameter == 1.75:
        costPerMOfFil = fil.priceperroll / db.session.query(Filament).filter(Filament.id==order.filamentfk).first().type_rel.m_in_1kg_175
    else:
        costPerMOfFil = fil.priceperroll / db.session.query(Filament).filter(Filament.id==order.filamentfk).first().type_rel.m_in_1kg_3
    
    l_in_m = float(filused.strip().replace('m',''))
    c_materials = costPerMOfFil * l_in_m

    #MARKUP ON MATERIALS COSTING
    custmarkup = db.session.query(Customer.markuppercent).filter(Customer.id == order.customerfk).scalar()
    c_materials_markup = custmarkup * c_materials
    
    #LABOR COSTING
    totaltime = order.setuptime + order.taredowntime
    pricePerMin = db.session.query(Customer).filter(Customer.id==order.customerfk).first().laborperhour / 60
    c_labor = pricePerMin * totaltime
    
    #MACHINE COSTING
    c_machine = 0
   
    return {'materials':c_materials, 'markup':c_materials_markup, 'labor':c_labor, 'machine':c_machine}

def calc_total_time(labortime, time):
    labortime = labortime * 60
    labortime = labortime + time 
    return calculate_print_time(labortime)