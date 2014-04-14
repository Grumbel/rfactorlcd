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


from construct import Struct, UBInt8, SLInt16, SLInt32, LFloat32, Array, PascalString

import rfactorlcd


class WheelState(object):

    def __init__(self):
        pass


class VehicleState(object):

    def __init__(self):
        pass


Vect = lambda name: Struct(name,  LFloat32("x"), LFloat32("y"), LFloat32("z"))

InfoMessage = Struct("info",
                     PascalString("track_name"),
                     PascalString("player_name"),
                     PascalString("plr_file_name"),
                     LFloat32("end_e_t"),
                     SLInt32("max_laps"),
                     LFloat32("lap_dist"))

ScoreMessage = Struct("score",
                      UBInt8("game_phase"),
                      UBInt8("yellow_flag_state"),
                      Array(3, UBInt8("sector_flag")),
                      UBInt8("start_light"),
                      UBInt8("num_red_lights"),
                      SLInt32("session"),
                      LFloat32("current_e_t"),
                      LFloat32("ambient_temp"),
                      LFloat32("track_temp"))

VehicleMessage = Struct("vehicles",
                        SLInt32("num_vehicles"),
                        Array(lambda ctx: ctx.num_vehicles,
                              Struct("vehicle",
                                     UBInt8("is_player"),
                                     PascalString("driver_name"),
                                     PascalString("vehicle_name"),
                                     PascalString("vehicle_class"),
                                     SLInt16("total_laps"),

                                     UBInt8("in_pits"),
                                     UBInt8("place"),
                                     LFloat32("time_behind_next"),
                                     SLInt32("laps_behind_next"),
                                     LFloat32("time_behind_leader"),
                                     SLInt32("laps_behind_leader"),

                                     LFloat32("best_sector1"),
                                     LFloat32("best_sector2"),
                                     LFloat32("best_lap_time"),
                                     LFloat32("last_sector1"),
                                     LFloat32("last_sector2"),
                                     LFloat32("last_lap_time"),
                                     LFloat32("cur_sector1"),
                                     LFloat32("cur_sector2"),

                                     SLInt16("num_pitstops"),
                                     SLInt16("num_penalties"),

                                     LFloat32("lap_start_et"))))

TelemetryMessage = Struct("telemetry",
                          SLInt32("lap_number"),
                          LFloat32("lap_start_et"),

                          Vect("pos"),
                          Vect("local_vel"),
                          Vect("local_accel"),

                          Vect("ori_x"),
                          Vect("ori_y"),
                          Vect("ori_z"),
                          Vect("local_rot"),
                          Vect("local_rot_accel"),

                          SLInt32("gear"),
                          LFloat32("rpm"),
                          LFloat32("max_rpm"),
                          LFloat32("clutch_rpm"),

                          LFloat32("fuel"),
                          LFloat32("water_temp"),
                          LFloat32("oil_temp"),

                          LFloat32("throttle"),
                          LFloat32("brake"),
                          LFloat32("steering"),
                          LFloat32("clutch"),

                          LFloat32("steering_arm_force"),

                          UBInt8("scheduled_stops"),
                          UBInt8("overheating"),
                          UBInt8("detached"),

                          Array(8, UBInt8("dent_severity")),

                          Array(4,
                                Struct("wheel",
                                       LFloat32("rotation"),
                                       LFloat32("suspension_deflection"),
                                       LFloat32("ride_height"),
                                       LFloat32("tire_load"),
                                       LFloat32("lateral_force"),
                                       LFloat32("grip_fract"),
                                       LFloat32("brake_temp"),
                                       LFloat32("pressure"),
                                       Array(3, LFloat32("temperatur")),
                                       LFloat32("wear"),
                                       UBInt8("surface_type"),
                                       UBInt8("flat"),
                                       UBInt8("detached"))))


class rFactorState(object):

    def __init__(self):
        self.telemetry = None
        self.vehicles = None
        self.score = None
        self.info = None

    def on_telemetry(self, msg):
        self.telemetry = TelemetryMessage.parse(msg)

    def on_vehicle(self, msg):
        self.vehicles = VehicleMessage.parse(msg)

    def on_score(self, msg):
        self.score = ScoreMessage.parse(msg)

    def on_info(self, msg):
        self.info = InfoMessage.parse(msg)

    def on_start_realtime(self, msg):
        pass

    def on_end_realtime(self, msg):
        pass

    def on_start_session(self, msg):
        pass

    def on_end_session(self, msg):
        pass

    def dispatch_message(self, tag, payload):
        if tag == "STSS":
            self.on_start_session(payload)
        elif tag == "EDSS":
            self.on_end_session(payload)
        elif tag == "STRT":
            self.on_start_realtime(payload)
        elif tag == "EDRT":
            self.on_end_realtime(payload)
        elif tag == "VHCL":
            self.on_vehicle(payload)
        elif tag == "TLMT":
            self.on_telemetry(payload)
        elif tag == "SCOR":
            self.on_score(payload)
        elif tag == "INFO":
            self.on_info(payload)
        else:
            print "error: unhandled tag: %s" % tag


# EOF #
