from printing import db


def get_raw_data():
    # return filament used, time to print
    with open("Humulin u500.gcode", "r") as file:
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
    formattedweight = calculate_weight(filused)
    return [formattedtime, formattedweight]


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


def calculate_weight(weightinm):
    import math

    diameter = 1.75
    density = 1.24
    # Volume = (length in m * 100) * pi() * ((diam/2)^2)
    filused = float(weightinm.strip("\n").replace("m", ""))
    filcm = filused * 100
    radius = (diameter / 2) / 10
    csarea = math.pi * (radius) ** 2
    volume = filcm * csarea
    weight = volume * density
    weight = f"{round(weight)}g"
    return weight
