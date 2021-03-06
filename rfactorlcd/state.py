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


import logging

import rfactorlcd


class LapTime:
    def __init__(self):
        self.sector1 = 0
        self.sector2 = 0
        self.sector3 = 0

    @property
    def total(self):
        return self.sector1 + self.sector2 + self.sector3


class LapTimes(object):
    """Lap time history for a vehicle in a single session"""

    def __init__(self):
        self.laps = {}
        self.current_sector = None

    @property
    def best_time(self):
        if self.laps == []:
            return 0
        else:
            return min([lap.total for lap in self.laps])

    def last_lap(self):
        last_lap = -1
        last_times = None
        for lap, times in self.laps.items():
            if lap > last_lap:
                last_lap = lap
                last_times = times
        return last_times

    def update(self, state):
        """Update current LapTime history with info from VehicleState"""

        if state.sector == 0 and state.total_laps == 0:
            pass

        elif self.current_sector != state.sector:
            self.current_sector = state.sector

            if state.sector == 0:
                lap = state.total_laps - 1
            else:
                lap = state.total_laps

            if lap in self.laps:
                lap_time = self.laps[lap]
            else:
                lap_time = LapTime()
                self.laps[lap] = lap_time

            # set the sector time in the LapTime object
            if state.sector == 1:
                lap_time.sector1 = state.cur_sector1
            elif state.sector == 2:
                lap_time.sector2 = state.cur_sector2 - state.cur_sector1
            elif state.sector == 0:
                lap_time.sector3 = state.last_lap_time - state.cur_sector2
            else:
                logging.error("unknown sector: %d" % state.sector)


class WheelState(object):

    def __init__(self):
        self.rotation = 0.0
        self.suspension_deflection = 0.0
        self.ride_height = 0.0
        self.tire_load = 0.0
        self.lateral_force = 0.0
        self.grip_fract = 0.0
        self.brake_temp = 0.0
        self.pressure = 0.0
        self.temperature = [0.0, 0.0, 0.0]
        self.wear = 0.0
        self.surface_type = 0
        self.flat = 0
        self.detached = 0


class VehicleState(object):

    def __init__(self):
        self.is_player = 0
        self.control = 0
        self.driver_name = ""
        self.vehicle_name = ""
        self.vehicle_class = ""
        self.total_laps = 0

        self.sector = 0
        self.finish_status = 0
        self.lap_dist = 0
        self.path_lateral = 0.0
        self.track_edge = 0.0

        self.in_pits = 0
        self.place = 0
        self.time_behind_next = 0.0
        self.laps_behind_next = 0
        self.time_behind_leader = 0.0
        self.laps_behind_leader = 0

        self.best_sector1 = 0.0
        self.best_sector2 = 0.0
        self.best_lap_time = 0.0
        self.last_sector1 = 0.0
        self.last_sector2 = 0.0
        self.last_lap_time = 0.0
        self.cur_sector1 = 0.0
        self.cur_sector2 = 0.0

        self.num_pitstops = 0
        self.num_penalties = 0

        self.lap_start_et = 0.0

        self.lap_times = LapTimes()


class rFactorState(object):

    def __init__(self):
        self.session_id = 0

        # telemetry defaults
        self.lap_number = 0
        self.lap_start_et = 0.0

        self.pos = (0.0, 0.0, 0.0)
        self.local_vel = (0.0, 0.0, 0.0)
        self.local_accel = (0.0, 0.0, 0.0)

        self.ori_x = (0.0, 0.0, 0.0)
        self.ori_y = (0.0, 0.0, 0.0)
        self.ori_z = (0.0, 0.0, 0.0)
        self.local_rot = (0.0, 0.0, 0.0)
        self.local_rot_accel = (0.0, 0.0, 0.0)

        self.gear = 0
        self.rpm = 0.0
        self.max_rpm = 0.0
        self.clutch_rpm = 0.0

        self.fuel = 0.0
        self.water_temp = 0.0
        self.oil_temp = 0.0

        self.throttle = 0.0
        self.brake = 0.0
        self.steering = 0.0
        self.clutch = 0.0

        self.steering_arm_force = 0.0

        self.scheduled_stops = 0
        self.overheating = 0
        self.detached = 0

        self.dent_severity = [0, 0, 0, 0, 0, 0, 0, 0]

        self.wheels = [WheelState(), WheelState(), WheelState(), WheelState()]

        self.num_vehicles = 0
        self.player = None
        self.vehicles = []

        # info
        self.track_name = ""
        self.player_name = ""
        self.plr_file_name = ""
        self.end_e_t = 0.0
        self.max_laps = 0
        self.lap_dist = 1.0

        # score
        self.game_phase = 0
        self.yellow_flag_state = 0
        self.sector_flag = [0, 0, 0]
        self.start_light = 0
        self.num_red_lights = 0
        self.session = 0
        self.current_e_t = 0.0
        self.ambient_temp = 0.0
        self.track_temp = 0.0

        # Backward compatibility hacks:
        self.speed = 0
        self.laptime = "1:23:45"

        self.best_lap_driver = ""

    @property
    def best_lap_time(self):
        if self.vehicles != []:
            best = self.vehicles[0].best_lap_time
            for veh in self.vehicles[1:]:
                if veh.best_lap_time < best:
                    best = veh.best_lap_time
                    self.best_lap_driver = veh.driver_name  # FIXME: hack
            return best
        else:
            return 0

    def on_telemetry(self, msg):
        self.delta_time = msg.read_float()
        self.lap_number = msg.read_int()
        self.lap_start_et = msg.read_float()
        # missing: mVehicleName[64]
        # missing: mTrackName[64]

        self.pos = msg.read_vect()
        self.local_vel = msg.read_vect()
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

        self.last_impact_e_t = msg.read_float()
        self.last_impact_magnitude = msg.read_float()
        self.last_impact_pos = msg.read_vect()

        # give speed in km/h
        self.speed = -self.local_vel[2] * 3.6

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
            # missing: mTerrainName[16]
            self.wheels[i].surface_type = msg.read_char()
            self.wheels[i].flat = msg.read_char()
            self.wheels[i].detached = msg.read_char()

    def on_vehicle(self, msg):
        self.num_vehicles = msg.read_int()

        if self.num_vehicles != len(self.vehicles):
            self.vehicles = []
            for i in range(self.num_vehicles):
                self.vehicles.append(VehicleState())

        for i in range(0, self.num_vehicles):
            self.vehicles[i].is_player = msg.read_char()
            self.vehicles[i].control = msg.read_char()

            self.vehicles[i].driver_name = msg.read_string()
            self.vehicles[i].vehicle_name = msg.read_string()
            self.vehicles[i].vehicle_class = msg.read_string()
            self.vehicles[i].total_laps = msg.read_short()

            # rFactor numbers sectors 1, 2, 0, convert them to 0, 1, 2
            self.vehicles[i].sector = (msg.read_char() + 2) % 3

            self.vehicles[i].finish_status = msg.read_char()
            self.vehicles[i].lap_dist = msg.read_float()
            self.vehicles[i].path_lateral = msg.read_float()
            self.vehicles[i].track_edge = msg.read_float()

            self.vehicles[i].in_pits = msg.read_char()
            self.vehicles[i].place = msg.read_char()
            self.vehicles[i].time_behind_next = msg.read_float()
            self.vehicles[i].laps_behind_next = msg.read_int()
            self.vehicles[i].time_behind_leader = msg.read_float()
            self.vehicles[i].laps_behind_leader = msg.read_int()

            self.vehicles[i].best_sector1 = msg.read_float()
            self.vehicles[i].best_sector2 = msg.read_float()
            self.vehicles[i].best_lap_time = msg.read_float()

            # these times are only updated going into a new lap
            self.vehicles[i].last_sector1 = msg.read_float()
            self.vehicles[i].last_sector2 = msg.read_float()
            self.vehicles[i].last_lap_time = msg.read_float()

            self.vehicles[i].cur_sector1 = msg.read_float()
            self.vehicles[i].cur_sector2 = msg.read_float()

            self.vehicles[i].num_pitstops = msg.read_short()
            self.vehicles[i].num_penalties = msg.read_short()

            self.vehicles[i].lap_start_et = msg.read_float()

            self.vehicles[i].pos = msg.read_vect()
            self.vehicles[i].local_vel = msg.read_vect()
            self.vehicles[i].local_accel = msg.read_vect()

            self.vehicles[i].ori_x = msg.read_vect()
            self.vehicles[i].ori_y = msg.read_vect()
            self.vehicles[i].ori_z = msg.read_vect()
            self.vehicles[i].local_rot = msg.read_vect()
            self.vehicles[i].local_rot_accel = msg.read_vect()

            if self.vehicles[i].is_player:
                self.player = self.vehicles[i]

            self.vehicles[i].lap_times.update(self.vehicles[i])

    def on_score(self, msg):
        self.game_phase = msg.read_char()
        self.yellow_flag_state = msg.read_char()
        self.sector_flag = msg.read_multi_char(3)
        self.start_light = msg.read_char()
        self.num_red_lights = msg.read_char()
        self.in_realtime = msg.read_char()
        self.session = msg.read_int()
        self.current_e_t = msg.read_float()
        self.ambient_temp = msg.read_float()
        self.track_temp = msg.read_float()
        self.dark_cloud = msg.read_float()
        self.raining = msg.read_float()
        self.wind = msg.read_vect()
        self.on_path_wetness = msg.read_float()
        self.off_path_wetness = msg.read_float()

    def on_info(self, msg):
        self.track_name = msg.read_string()
        self.player_name = msg.read_string()
        self.plr_file_name = msg.read_string()
        self.end_e_t = msg.read_float()
        self.max_laps = msg.read_int()
        self.lap_dist = msg.read_float()
        # missing mResultsStream

    def on_start_realtime(self, msg):
        pass

    def on_end_realtime(self, msg):
        pass

    def on_start_session(self, msg):
        self.session_id += 1
        self.vehicles = []
        logging.info("on_start_session")

    def on_end_session(self, msg):
        logging.info("on_end_session")

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
