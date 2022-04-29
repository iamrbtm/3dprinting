from printing import db
from printing.models import *

def set_init_length(filId, typefk, diameter, length):
    fil = db.session.query(Filament).filter(Filament.id == filId).first()
    diamvalues = db.session.query(Type).filter(Type.id == typefk).first()
    
    if diameter == "1.75" and length == 2: #length in m of 1kg of 1.75mm diameter
        init_value = diamvalues.m_in_1kg_175
    elif diameter == "3" and length == 2: #length in m of 1kg of 3mm diameter
        init_value = diamvalues.m_in_1kg_3
    elif diameter == "1.75" and length == 1: #length in m of 200g of 1.75mm diameter
       init_value = diamvalues.g_per_m_175 * 200
    elif diameter == "3" and length == 1: #length in m of 200g of 3mm diameter
        init_value = 0
    elif diameter == "1.75" and length == 3: #length in m of 2kg of 1.75mm diameter
        init_value = diamvalues.m_in_1kg_175 * 2
    elif diameter == "3" and length == 3: #length in m of 2kg of 3mm diameter
        init_value = diamvalues.m_in_1kg_3 * 2
    else:
        init_value = 0
        
    fil.aprox_remaining_length = init_value
    db.session.commit()
    
    return init_value
    
def update_fil_remaining(filId, amountConsumed):
    fil = db.session.query(Filament).filter(Filament.id == filId).first()
    fil.aprox_remaining_length = float(fil.aprox_remaining_length) - float(amountConsumed)
    db.session.commit()
    
def manual_adjust_length(filId, percentRemain):
    fil = db.session.query(Filament).filter(Filament.id == filId).first()
    remaining = float(fil.aprox_remaining_length) * (int(percentRemain)/100)
    fil.aprox_remaining_length = remaining
    db.session.commit()