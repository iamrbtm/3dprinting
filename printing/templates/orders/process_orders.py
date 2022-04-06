from printing import db, uploads
from printing.models import *


def get_raw_data(filament, file):
    # return filament used, time to print
    ulfile = uploads.save(file)
    with open ('printing/static/uploads/'+ulfile, 'r') as file:
        i = 0
        for line in file:
            if "used" in line:
                filused = line.replace(";Filament used: ", "")
            elif "TIME" in line:
                time = line.replace(";TIME:", "")
            i += 1
            if i >= 20:
                break
        print(filused, time)

    formattedtime = calculate_print_time(time)
    formattedweight = calculate_weight(filused, filament)
    return [formattedtime, formattedweight, filused]


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
        result = f"{minutes} minutes {seconds} seconds"
    elif day == 0 and hour > 0:
        result = f"{hour} hours {minutes} minutes {seconds} seconds"
    elif day > 0:
        if day == 1:
            result = f"{day} day {hour} hours {minutes} minutes {seconds} seconds"
        else:
            result = f"{day} days {hour} hours {minutes} minutes {seconds} seconds"
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
    pricePerMin = db.session.query(Setup).first().pricePerHour / 60
    c_labor = pricePerMin * totaltime
    
    #MACHINE COSTING
    
    c_machine = 0
    
    #SUB TOTAL
    c_subtotal = c_materials + c_materials_markup + c_labor + c_machine
   
    return {'materials':c_materials, 'markup':c_materials_markup, 'labor':c_labor, 'machine':c_machine, 'subtotal':c_subtotal}