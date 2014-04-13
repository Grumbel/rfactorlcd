#!/usr/bin/env python

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


import struct
import socket

import rfactorlcd


class rFactorLCDClient(object):

    def __init__(self):
        self.host = "duo"
        self.port = 4580

    def on_start_session(self, msg):
        print "[start_session]"

    def on_end_session(self, msg):
        print "[end_session]"

    def on_start_realtime(self, msg):
        print "[start_realtime]"

    def on_end_realtime(self, msg):
        print "[end_realtime]"

    def on_telemetry(self, msg):
        print "[telemetry]"
        print "info.mGear", msg.read_int()
        print "info.mEngineRPM", msg.read_float()
        print "info.mEngineMaxRPM", msg.read_float()
        print "info.mClutchRPM", msg.read_float()

        print "info.mFuel", msg.read_float()
        print "info.mEngineWaterTemp", msg.read_float()
        print "info.mEngineOilTemp", msg.read_float()

        print "info.mUnfilteredThrottle", msg.read_float()
        print "info.mUnfilteredBrake", msg.read_float()
        print "info.mUnfilteredSteering", msg.read_float()
        print "info.mUnfilteredClutch", msg.read_float()

        print "info.mSteeringArmForce", msg.read_float()

        for i in range(0, 8):
            print "info.mDentSeverity[%d]" % i, msg.read_char()

        for i in range(0, 4):
            print "wheel.mRotation", msg.read_float()
            print "wheel.mSuspensionDeflection", msg.read_float()
            print "wheel.mRideHeight", msg.read_float()
            print "wheel.mTireLoad", msg.read_float()
            print "wheel.mLateralForce", msg.read_float()
            print "wheel.mGripFract", msg.read_float()
            print "wheel.mBrakeTemp", msg.read_float()
            print "wheel.mPressure", msg.read_float()
            print "wheel.mTemperature[0]", msg.read_float()
            print "wheel.mTemperature[1]", msg.read_float()
            print "wheel.mTemperature[2]", msg.read_float()

            print "wheel.mWear", msg.read_float()
            print "wheel.mSurfaceType", msg.read_char()
            print "wheel.mFlat", msg.read_char()
            print "wheel.mDetached", msg.read_char()

    def on_vehicle(self, msg):
        print "[vehicle]"
        num_vehicles = msg.read_int()
        print "info.mNumVehicles", num_vehicles

        for i in range(0, num_vehicles):
            print "veh.mIsPlayer", msg.read_char()
            print "veh.mDriverName", msg.read_string()
            print "veh.mVehicleName", msg.read_string()
            print "veh.mVehicleClass", msg.read_string()
            print "veh.mTotalLaps", msg.read_short()

            print "veh.mInPits", msg.read_char()
            print "veh.mPlace", msg.read_char()
            print "veh.mTimeBehindNext", msg.read_float()
            print "veh.mLapsBehindNext", msg.read_int()
            print "veh.mTimeBehindLeader", msg.read_float()
            print "veh.mLapsBehindLeader", msg.read_int()

            print "veh.mBestSector1", msg.read_float()
            print "veh.mBestSector2", msg.read_float()
            print "veh.mBestLapTime", msg.read_float()
            print "veh.mLastSector1", msg.read_float()
            print "veh.mLastSector2", msg.read_float()
            print "veh.mLastLapTime", msg.read_float()
            print "veh.mCurSector1", msg.read_float()
            print "veh.mCurSector2", msg.read_float()

            print "veh.mNumPitstops", msg.read_short()
            print "veh.mNumPenalties", msg.read_short()

            print "veh.mLapStartET", msg.read_float()
            print "  ----------------"

    def on_score(self, msg):
        print "[score]"
        print "info.mGamePhase", msg.read_char()
        print "info.mYellowFlagState", msg.read_char()
        print "info.mSectorFlag[0]", msg.read_char()
        print "info.mSectorFlag[1]", msg.read_char()
        print "info.mSectorFlag[2]", msg.read_char()
        print "info.mStartLight", msg.read_char()
        print "info.mNumRedLights", msg.read_char()
        print "info.mSession", msg.read_int()
        print "info.mCurrentET", msg.read_float()
        print "info.mAmbientTemp", msg.read_float()
        print "info.mTrackTemp", msg.read_float()

    def on_info(self, msg):
        print "[info]"
        print "info.mTrackName", msg.read_string()
        print "info.mPlayerName", msg.read_string()
        print "info.mPlrFileName", msg.read_string()
        print "info.mEndET", msg.read_float()
        print "info.mMaxLaps", msg.read_int()
        print "info.mLapDist", msg.read_float()

    def dispatch_message(self, tag, payload):
        # print tag, size
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

    def main(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Connecting to %s:%s" % (self.host, self.port)
            self.sock.connect((self.host, self.port))
            stream = ""
            while True:
                self.sock.sendall("\n")
                stream += self.sock.recv(4096 * 4)
                if len(stream) >= 8:
                    tag, size = struct.unpack_from("4sI", stream)
                    if len(stream) >= size:
                        payload = stream[8:size]
                        stream = stream[size:]
                        self.dispatch_message(tag, payload)
        finally:
            self.sock.close()


if __name__ == '__main__':
    app = rFactorLCDClient()
    app.main()


# EOF #
