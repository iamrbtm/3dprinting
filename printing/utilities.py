import re
from printing import db
from printing.models import *


def format_tel(phone):
    if phone != "":
        clean_phone = re.sub("[^0-9]+", "", phone)
        formatted_phone = (
            re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone[:-1]))
            + clean_phone[-1]
        )
        return formatted_phone
    else:
        return ""


def populate_states():
    states = [
        ["Alabama", "AL"],
        ["Alaska", "AK"],
        ["Arizona", "AZ"],
        ["Arkansas", "AR"],
        ["California", "CA"],
        ["Colorado", "CO"],
        ["Connecticut", "CT"],
        ["Delaware", "DE"],
        ["District Of Columbia", "DC"],
        ["Florida", "FL"],
        ["Georgia", "GA"],
        ["Hawaii", "HI"],
        ["Idaho", "ID"],
        ["Illinois", "IL"],
        ["Indiana", "IN"],
        ["Iowa", "IA"],
        ["Kansas", "KS"],
        ["Kentucky", "KY"],
        ["Louisiana", "LA"],
        ["Maine", "ME"],
        ["Maryland", "MD"],
        ["Massachusetts", "MA"],
        ["Michigan", "MI"],
        ["Minnesota", "MN"],
        ["Mississippi", "MS"],
        ["Missouri", "MO"],
        ["Montana", "MT"],
        ["Nebraska", "NE"],
        ["Nevada", "NV"],
        ["New Hampshire", "NH"],
        ["New Jersey", "NJ"],
        ["New Mexico", "NM"],
        ["New York", "NY"],
        ["North Carolina", "NC"],
        ["North Dakota", "ND"],
        ["Ohio", "OH"],
        ["Oklahoma", "OK"],
        ["Oregon", "OR"],
        ["Pennsylvania", "PA"],
        ["Rhode Island", "RI"],
        ["South Carolina", "SC"],
        ["South Dakota", "SD"],
        ["Tennessee", "TN"],
        ["Texas", "TX"],
        ["Utah", "UT"],
        ["Vermont", "VT"],
        ["Virginia", "VA"],
        ["Washington", "WA"],
        ["West Virginia", "WV"],
        ["Wisconsin", "WI"],
        ["Wyoming", "WY"],
    ]

    if len(states) != States.query.count():
        for st in states:
            abr = st[1]
            state = st[0]

            cnt = States.query.filter(States.abr == abr).count()
            if cnt == 0:
                new = States(abr=abr, state=state)
                db.session.add(new)
                db.session.commit()


def populate_types():
    filtypes = [
        [
            "ABS",
            "Making durable parts that need to withstand higher temperatures, Easy to print with, strong plastic",
            "Legos, instruments, sports equipment, Objects that might be dropped, knife handles, car phone mounts, phone cases, toys, wedding rings",
            "210 - 250",
            "80-110 ",
            "Kapton Tape / Hairspray",
            "1.75mm/3mm",
        ],
        [
            "PLA",
            "Odorless, Low-warp, Eco-Friendly, Less energy to process",
            "Food containers such as candy wrappers, biodegradable medical implants, models, prototype parts",
            "190 - 230",
            "60 - 80.",
            "Blue painter's tape/ Hairspray",
            "1.75mm/3mm",
        ],
        [
            "PVA",
            "Non harmful, non-toxic, and environment friendly, Easily be dissolved in water under normal temperature, Easily stripping.",
            "paper adhesive, thickener, packaging film in feminine hygiene, adult incontinence products, children's play putty or slime, freshwater sports fishing",
            "180 - 230",
            "45 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "PET",
            "FDA approved for food containers and tools used for food consumption, barely warps, no odors or fumes when printed",
            "phone cases and mechanical parts that require flexibility and impact resistance, jewelry, props, and electronics",
            "230-255 ",
            "55 -70 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "PETG",
            "Extremely durable and prints without odor. Has superior impact resistance that is superior to PET. Low shrinkage, no warping and not brittle.",
            "Protective components like phone cases and mechanical parts that require flexibility. Food containers like cups and plates.",
            "220 - 245",
            "70 - 75",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "PETT",
            "Colorless, Water Clear, FDA approved, Recyclable, Strong and Flexible",
            "Food containers like cups and utensils, Soda pop bottles",
            "210 - 230",
            "45 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "HIPS",
            "Biodegradable, Great 3D Support material, low-cost",
            "costumes, models, miniature figurines, prototyping",
            "220-230 ",
            "50 -60 ",
            "Kapton Tape/Hairspray",
            "1.75mm/3mm",
        ],
        [
            "Nylon",
            "strong, lightweight, durable, flexible, wear-resistant, 100% thermoplastic",
            "machine parts, mechanical components, structural parts, gears and bearings, dynamic load, containers, tools, consumer products and toys.",
            "210 - 250",
            "60 -80 ",
            "PVA Based Glue",
            "1.75mm/3mm",
        ],
        [
            "Wood",
            "Versatility, Real wood scent, Durability, contain real wood fibers",
            "wooden box, wooden figurine, tables, chairs, cups or the likes.",
            "200 - 260",
            "90-110.",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Sandstone",
            "No plastic feeling, Printed objects can be coloured and easely grinded, Stics well on print bed, No heated bed necessary, Near zero warp",
            "Architecture models, landscapes",
            "165 - 210",
            "20 -55 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Metal",
            "highly durable, not soluble, little shrinkage during cooling",
            "Jewelry, statues, home hardware and artifact replicas.",
            "195-220 ",
            "50 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Magnetic Iron PLA",
            "High Durability, Magnetic Look, Magnetic properties",
            "Fridge magnets, sensors, actuators, magnetic stirrers, and educational, DIY projects.",
            "185 ",
            "20 -55 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Conductive PLA",
            "Very low warping, Not Soluble, Print low-voltage electronic circuits",
            "low-voltage circuitry applications, touch sensor projects",
            "225-260 ",
            "90 -110 ",
            "Kapton Tape/ Haispray",
            "1.75mm/3mm",
        ],
        [
            "Carbon Fiber",
            "Highly Durable, Soluble, Low Warpage, Good layer adhesion",
            "Frames, supports, propellers, tools, mechanical parts, protective casings, shells, high durability applications",
            "195-220 ",
            "50 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Flexible/TPE",
            "Flexible 3D printing material, excellent abrasion resistance, smooth feeding properties, Durability",
            "Toys, novelty items, wearable, phone cases, visual products.",
            "210-225 ",
            "20-55 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Glow In The Dark",
            "Minimal Warping, Glow in the Dark properties, durable, not soluble, low shrinkage during cooling",
            "children's toys, novelty items, wearables, phone cases, visual products.",
            "185-205 ",
            "70 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
        [
            "Amphora",
            "High strength and very high toughness, FDA food contact compliance, Odor Neutral processing, Styrene free formulation",
            "Desktop items, Mechanical Parts",
            "220 - 250",
            "60 - 70 ",
            "Blue Painters Tape",
            "1.75mm/3mm",
        ],
    ]

    if len(filtypes) != Type.query.count():
        for fil in filtypes:
            typename = fil[0]
            cnt = Type.query.filter(Type.type == typename).count()
            if cnt == 0:
                etemp = list(map(str.strip, fil[3].split("-")))
                bedtemp = list(map(str.strip, fil[4].split("-")))
                adh = list(map(str.strip, fil[5].split("/")))
                diam = list(map(str.strip, fil[6].split("/")))
                use = list(map(str.strip, fil[2].split(",")))
                prop = list(map(str.strip, fil[1].split(",")))

                new = Type(
                    type=typename,
                    properties=prop,
                    useage=use,
                    extruder_temp=etemp,
                    bed_temp=bedtemp,
                    bed_adhesion=adh,
                    diameter=diam,
                )
                db.session.add(new)
                db.session.commit()


# if __name__ == "__main__":
#     populate_types()
