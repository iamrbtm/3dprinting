from printing import db
from printing.models import *
from printing.templates.orders.gcode import *
from flask_login import current_user


class Ordering:
    def __init__(
        self,
        filamentfk,
        setuptime,
        taredowntime,
        postprocessingtime,
        customerfk,
        machinefk,
        order_status,
        date_needed,
        project_name,
        qty,
        gcode,
    ):

        self.filamentfk = filamentfk
        self.postprocessingtime = postprocessingtime
        self.setuptime = setuptime
        self.taredowntime = taredowntime
        self.customerfk = customerfk
        self.machinefk = machinefk
        self.date_needed = date_needed
        self.project_name = project_name
        self.qty = qty
        self.order_status = order_status
        self.gcode = gcode
        self.userid = current_user.id

        # GCode Processing
        gc = Gcode(self.gcode, self.filamentfk)
        self.filused = float(gc.filused.strip("\n").replace("m", ""))
        self.time = int(gc.time.strip("\n"))

        # Self Processing
        self.time_to_print = self.calculate_print_time()
        self.weight_in_g = self.calculate_weight()
        self.c_materials = self.cost_materials()
        self.c_labor = self.cost_labor()
        self.c_markup = self.cost_markup()
        self.c_machine = self.cost_machine()
        self.shipping = self.calculate_shipping()
        self.subtotal = self.subtotal()
        self.total = self.total()

    def update_costs(self):
        self.c_materials = self.cost_materials()
        self.c_labor = self.cost_labor()
        self.c_markup = self.cost_markup()
        self.c_machine = self.cost_machine()
        self.shipping = self.calculate_shipping()
        self.send_to_db()

    def cost_materials(self):
        fil = (
            db.session.query(Filament)
            .filter(Filament.id == self.filamentfk)
            .first_or_404()
        )
        pricePerM = float(fil.priceperroll / 1000)
        return float(self.filused) * pricePerM

    def cost_labor(self):
        def calculate_total_labor(self):
            return int(
                int(self.setuptime)
                + int(self.taredowntime)
                + int(self.postprocessingtime)
            )

        def labor_cost_per_min(self, priceperhour):
            return float(int(priceperhour) / 60)

        return calculate_total_labor(self) * labor_cost_per_min(self, 20)

    def cost_machine(self):
        return 0

    def cost_markup(self):
        cust = Customer.query.filter(Customer.id == self.customerfk).first_or_404()
        return self.c_materials * float(cust.markuppercent)

    def calculate_shipping(self):
        cust = Customer.query.get_or_404(self.customerfk)

        return 0

    def update_status(self):
        pass

    def add_to_db(self):
        order = Orders(
            date_needed=self.date_needed,
            project_name=self.project_name,
            qty=self.qty,
            weight_in_g=self.weight_in_g,
            time_to_print=self.time_to_print,
            setuptime=self.setuptime,
            taredowntime=self.taredowntime,
            postprocessingtime=self.postprocessingtime,
            time=self.time,
            filused=self.filused,
            c_labor=self.c_labor,
            c_machine=self.c_machine,
            c_materials=self.c_materials,
            c_markup=self.c_markup,
            shipping=self.shipping,
            userid=self.userid,
            gcodefilename=self.gcode,
            customerfk=self.customerfk,
            order_status=self.order_status,
            machinefk=self.machinefk,
            filamentfk=self.filamentfk,
        )
        db.session.add(order)
        db.session.commit()

    def send_to_db(self):
        order = Orders.query.filter(Orders.project_name == self.project_name).first()
        order.date_needed = (self.date_needed,)
        order.project_name = (self.project_name,)
        order.qty = (self.qty,)
        order.weight_in_g = (self.weight_in_g,)
        order.time_to_print = (self.time_to_print,)
        order.setuptime = (self.setuptime,)
        order.taredowntime = (self.taredowntime,)
        order.postprocessingtime = (self.postprocessingtime,)
        order.time = (self.time,)
        order.filused = (self.filused,)
        order.c_labor = (self.c_labor,)
        order.c_machine = (self.c_machine,)
        order.c_materials = (self.c_materials,)
        order.c_markup = (self.c_markup,)
        order.shipping = (self.shipping,)
        order.userid = (self.userid,)
        order.gcodefilename = (self.gcode,)
        order.customerfk = (self.customerfk,)
        order.order_status = (self.order_status,)
        order.machinefk = (self.machinefk,)
        order.filamentfk = self.filamentfk
        db.session.commit()

    def calculate_print_time(self):
        timeinsec = self.time + (
            (self.setuptime + self.taredowntime + self.postprocessingtime) * 60
        )
        timeinsec = int(timeinsec)
        day = timeinsec // (24 * 3600)
        timeinsec = timeinsec % (24 * 3600)
        hour = timeinsec // 3600
        timeinsec %= 3600
        minutes = timeinsec // 60
        timeinsec %= 60
        seconds = timeinsec

        if day == 0 and hour == 0:
            result = f"00:{minutes}:{seconds}"
        elif day == 0 and hour > 0:
            result = f"{hour}:{minutes}:{seconds}"
        elif day > 0:
            result = f"{day} {hour}:{minutes}:{seconds}"
        else:
            result = "failed"
        return result

    def calculate_weight(self):
        import math

        diameter = (
            db.session.query(Filament.diameter)
            .filter(Filament.id == self.filamentfk)
            .scalar()
        )
        density = (
            db.session.query(Filament)
            .filter(Filament.id == self.filamentfk)
            .first()
            .type_rel.densitygcm3
        )
        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filused = self.filused
        filcm = filused * 100
        radius = (diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * density
        weight = f"{round(weight)}g"
        return weight

    def subtotal(self):
        return self.c_labor + self.c_machine + self.c_markup + self.c_materials

    def total(self):
        return self.subtotal + self.shipping
