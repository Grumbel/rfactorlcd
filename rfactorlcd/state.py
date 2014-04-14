# rFactor Remote LCD
# Copyright (C) 2014 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import rfactorlcd


class WheelState(object):

    def __init__(self):
        pass


class VehicleState(object):

    def __init__(self):
        pass


class rFactorState(object):

    def __init__(self, data="15/17,1,0.107,1.438,1.658,21.598,29.738,31.855,1:23.190,0.0,0,30.0,63.4,26.9,0.0,0.0"):
        self.data = data

        cols = data.split(",")
        self.position = cols[0]
        self.running = int(cols[1])
        self.unknowns = cols[2:5]
        self.sector = cols[5:8]
        self.laptime = cols[8]
        self.speed = float(cols[9])
        self.gear = int(cols[10])
        self.fuel = float(cols[11])
        self.oil_temp = float(cols[12])
        self.water_temp = float(cols[13])
        self.rpm = float(cols[14])
        self.max_rpm = float(cols[15])

        self.wheels = [WheelState(), WheelState(), WheelState(), WheelState()]
        self.vehicles = []

    def to_vracingDisplayPRO(self):
        result = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            self.position,
            self.running,
            self.unknowns[0],
            self.unknowns[1],
            self.unknowns[2],
            self.sector[0],
            self.sector[1],
            self.sector[2],
            self.laptime,
            self.speed,
            self.gear,
            self.fuel,
            self.oil_temp,
            self.water_temp,
            self.rpm,
            self.max_rpm)

        # print "IN: ", self.data
        # print "OUT: ", result

        return result

    def on_telemetry(self, msg):
        self.lap_number = msg.read_int()
        self.lap_start_et = msg.read_float()

        self.pos = msg.read_vect()
        self.local_vel = msg.read_vect()
        self.speed = -self.local_vel[2]
        self.local_accel = msg.read_vect()

        self.ori_x = msg.read_vect()
        self.ori_y = msg.read_vect()
        self.ori_z = msg.read_vect()
        self.local_rot = msg.read_vect()
        self.local_rot_accel = msg.read_vect()

        self.gear = msg.read_int()
        self.rpm = msg.read_float()
        self.max_rpm = msg.read_float()
        self.clutch_rpm = msg.read_float()

        self.fuel = msg.read_float()
        self.water_temp = msg.read_float()
        self.oil_temp = msg.read_float()

        self.throttle = msg.read_float()
        self.brake = msg.read_float()
        self.steering = msg.read_float()
        self.clutch = msg.read_float()

        self.steering_arm_force = msg.read_float()

        self.scheduled_stops = msg.read_char()
        self.overheating = msg.read_char()
        self.detached = msg.read_char()

        self.dent_severity = msg.read_multi_char(8)

        for i in range(0, 4):
            self.wheels[i].rotation = msg.read_float()
            self.wheels[i].suspension_deflection = msg.read_float()
            self.wheels[i].ride_height = msg.read_float()
            self.wheels[i].tire_load = msg.read_float()
            self.wheels[i].lateral_force = msg.read_float()
            self.wheels[i].grip_fract = msg.read_float()
            self.wheels[i].brake_temp = msg.read_float()
            self.wheels[i].pressure = msg.read_float()
            self.wheels[i].temperature = [msg.read_float(),
                                          msg.read_float(),
                                          msg.read_float()]
            self.wheels[i].wear = msg.read_float()
            self.wheels[i].surface_type = msg.read_char()
            self.wheels[i].flat = msg.read_char()
            self.wheels[i].detached = msg.read_char()

    def on_vehicle(self, msg):
        self.num_vehicles = msg.read_int()

        if self.num_vehicles < len(self.vehicles):
            self.vehicles = self.vehicles[:self.num_vehicles]
        elif self.num_vehicles > len(self.vehicles):
            for i in range(self.num_vehicles - len(self.vehicles)):
                self.vehicles.append(VehicleState())

        for i in range(0, self.num_vehicles):
            self.vehicles[i].is_player = msg.read_char()
            self.vehicles[i].driver_name = msg.read_string()
            self.vehicles[i].vehicle_name = msg.read_string()
            self.vehicles[i].vehicle_class = msg.read_string()
            self.vehicles[i].total_laps = msg.read_short()

            self.vehicles[i].in_pits = msg.read_char()
            self.vehicles[i].place = msg.read_char()
            self.vehicles[i].time_behind_next = msg.read_float()
            self.vehicles[i].laps_behind_next = msg.read_int()
            self.vehicles[i].time_behind_leader = msg.read_float()
            self.vehicles[i].laps_behind_leader = msg.read_int()

            self.vehicles[i].best_sector1 = msg.read_float()
            self.vehicles[i].best_sector2 = msg.read_float()
            self.vehicles[i].best_lap_time = msg.read_float()
            self.vehicles[i].last_sector1 = msg.read_float()
            self.vehicles[i].last_sector2 = msg.read_float()
            self.vehicles[i].last_lap_time = msg.read_float()
            self.vehicles[i].cur_sector1 = msg.read_float()
            self.vehicles[i].cur_sector2 = msg.read_float()

            self.vehicles[i].num_pitstops = msg.read_short()
            self.vehicles[i].num_penalties = msg.read_short()

            self.vehicles[i].lap_start_et = msg.read_float()

    def on_score(self, msg):
        self.game_phase = msg.read_char()
        self.yellow_flag_state = msg.read_char()
        self.sector_flag = msg.read_multi_char(3)
        self.start_light = msg.read_char()
        self.num_red_lights = msg.read_char()
        self.session = msg.read_int()
        self.current_e_t = msg.read_float()
        self.ambient_temp = msg.read_float()
        self.track_temp = msg.read_float()

    def on_info(self, msg):
        self.track_name = msg.read_string()
        self.player_name = msg.read_string()
        self.plr_file_name = msg.read_string()
        self.end_e_t = msg.read_float()
        self.max_laps = msg.read_int()
        self.lap_dist = msg.read_float()

    def on_start_realtime(self, msg):
        pass

    def on_end_realtime(self, msg):
        pass

    def on_start_session(self, msg):
        pass

    def on_end_session(self, msg):
        pass

    def dispatch_message(self, tag, payload):
        msg = rfactorlcd.BinaryDecoder(payload)

        if tag == "STSS":
            self.on_start_session(msg)
        elif tag == "EDSS":
            self.on_end_session(msg)
        elif tag == "STRT":
            self.on_start_realtime(msg)
        elif tag == "EDRT":
            self.on_end_realtime(msg)
        elif tag == "VHCL":
            self.on_vehicle(msg)
        elif tag == "TLMT":
            self.on_telemetry(msg)
        elif tag == "SCOR":
            self.on_score(msg)
        elif tag == "INFO":
            self.on_info(msg)
        else:
            print "error: unhandled tag: %s" % tag


# EOF #
