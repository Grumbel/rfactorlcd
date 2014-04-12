// rFactor Remote LCD
// Copyright (C) 2014 Ingo Ruhnke <grumbel@gmail.com>
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation, either version 3 of
// the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this program. If not, see
// <http://www.gnu.org/licenses/>.


#include "rfactorlcd.hpp"

#include <algorithm>
#include <shlwapi.h>
#include <string.h>

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "shlwapi.lib")


#define FOURCC(a, b, c, d) ((a) | (b << 8) | (c << 16) | (d << 24))

#define START_SESSION_TAG FOURCC('S', 'T', 'S', 'S')
#define END_SESSION_TAG FOURCC('E', 'D', 'S', 'S')

#define START_REALTIME_TAG FOURCC('S', 'T', 'R', 'T')
#define END_REALTIME_TAG FOURCC('E', 'D', 'R', 'T')

#define TELEMETRY_TAG FOURCC('T', 'E', 'L', 'M')
#define SCORE_TAG FOURCC('S', 'C', 'O', 'R')

#define INFO_TAG FOURCC('I', 'N', 'F', 'O')
#define VEHICLE_TAG FOURCC('V', 'E', 'H', 'L')


InternalsPluginInfo g_PluginInfo;

// interface to plugin information
extern "C" __declspec(dllexport)
const char* __cdecl GetPluginName() { return "rfactorlcdPlugin 0.0.0"; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginVersion() { return 1; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginObjectCount() { return 1; }

extern "C" __declspec(dllexport)
PluginObjectInfo* __cdecl GetPluginObjectInfo(const unsigned uIndex)
{
  if (uIndex == 0)
  {
    return  &g_PluginInfo;
  }
  else
  {
    return 0;
  }
}

class NetworkMessage
{
private:
  union
  {
    char buffer[4096];
    struct {
      int tag;
      int size;
    } d;
  };

public:
  NetworkMessage(int tag) :
    buffer()
  {
    d.tag = tag;
    d.size = 8;
  }

  inline void write_string(const char* str)
  {
    // write Pascal like string with the first byte giving the length
    // of the string
    int len = strlen(str);
    buffer[d.size] = len;
    d.size += 1;
    memcpy(buffer + d.size, str, len);
    d.size += len;
  }

  inline void write_char(char v)
  {
    buffer[d.size] = v;
    d.size += sizeof(v);
  }

  inline void write_short(short v)
  {
    buffer[d.size] = v;
    d.size += sizeof(v);
  }

  inline void write_int(int v)
  {
    reinterpret_cast<int&>(buffer[d.size]) = v;
    d.size += sizeof(v);
  }

  inline void write_float(float v)
  {
    reinterpret_cast<float&>(buffer[d.size]) = v;
    d.size += sizeof(v);
  }

  inline const char* get_data() const
  {
    return buffer;
  }

  inline int get_size() const
  {
    return d.size;
  }
};

rFactorLCDPlugin::rFactorLCDPlugin() :
  m_ini_filename(),
  m_log_filename(),
  m_port(4580),
  m_out("C:\\rfactor_plugin.txt"),
  m_listen_socket(INVALID_SOCKET),
  m_client_sockets()
{
  init_filenames();
}

rFactorLCDPlugin::~rFactorLCDPlugin()
{
}

void
rFactorLCDPlugin::init_filenames()
{
  char path[MAX_PATH];
  int bytes = GetModuleFileNameA(NULL, path, MAX_PATH);
  if (bytes == 0)
  {
    m_out << "couldn't GetModuleFileNameA: " << GetLastError() << std::endl;
  }
  else
  {
    PathRemoveFileSpec(path);
    PathAppend(path, "\\Plugins");

    m_out << bytes << "Plugins path: " << path << std::endl;

    PathCombine(m_ini_filename, path, "rfactorlcd.ini");
    PathCombine(m_log_filename, path, "rfactorlcd.log");

    m_out << bytes << "log: " << m_ini_filename << std::endl;
    m_out << bytes << "ini: " << m_log_filename << std::endl;

    m_port = GetPrivateProfileInt("rfactorlcd", "port", m_port, m_ini_filename);

    m_out << bytes << "port: " << m_port << std::endl;
  }
}

void
rFactorLCDPlugin::Destroy()
{
  m_out << "destroy" << std::endl;
}

PluginObjectInfo*
rFactorLCDPlugin::GetInfo()
{
  return &g_PluginInfo;
}

void
rFactorLCDPlugin::setup_winsock()
{
  m_out << "setup_winsock" << std::endl;

  WSADATA wsaData;
  int ret = WSAStartup(MAKEWORD(2,2), &wsaData);
  if (ret != 0)
  {
    m_out << "error: WSAStartup failed: " << ret << std::endl;
    return;
  }
  else
  {
    struct addrinfo hints;
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    struct addrinfo* result_info = NULL;
    char port[32];
    sprintf(port, "%d", m_port);
    ret = getaddrinfo(NULL, port, &hints, &result_info);
    if (ret != 0)
    {
      m_out << "error: getaddrinfo failed: " << ret << std::endl;
      return;
    }

    m_listen_socket = socket(result_info->ai_family, result_info->ai_socktype, result_info->ai_protocol);
    if (m_listen_socket == INVALID_SOCKET)
    {
      m_out << "Error at socket(): " << WSAGetLastError() << std::endl;
      freeaddrinfo(result_info);
      return;
    }

    ret = bind(m_listen_socket, result_info->ai_addr, (int)result_info->ai_addrlen);
    if (ret == SOCKET_ERROR)
    {
      m_out << "bind failed with error: " << WSAGetLastError() << std::endl;
      freeaddrinfo(result_info);
      closesocket(m_listen_socket);
      m_listen_socket = INVALID_SOCKET;
      return;
    }
    else
    {
      freeaddrinfo(result_info);
    }

    if (listen(m_listen_socket, SOMAXCONN) == SOCKET_ERROR)
    {
      m_out << "Listen failed with error: " << WSAGetLastError() << std::endl;
      closesocket(m_listen_socket);
      m_listen_socket = INVALID_SOCKET;
      return;
    }

    // make m_listen_socket non-blocking
    u_long mode = 1;
    ret = ioctlsocket(m_listen_socket, FIONBIO, &mode);
    if (ret != 0)
    {
      m_out << "ioctlsocket() failed: " << ret << std::endl;
      closesocket(m_listen_socket);
      m_listen_socket = INVALID_SOCKET;
      return;
    }
  }
}

void
rFactorLCDPlugin::update_winsock()
{
  update_winsock_server();
  update_winsock_clients();
}

void
rFactorLCDPlugin::update_winsock_server()
{
  m_out << "update winsock server" << std::endl;
  if (m_listen_socket != INVALID_SOCKET)
  {
    SOCKET client_socket = accept(m_listen_socket, NULL, NULL);
    if (client_socket != INVALID_SOCKET)
    {
      u_long mode = 1;
      int ret = ioctlsocket(client_socket, FIONBIO, &mode);
      if (ret != 0)
      {
        m_out << "error: in update_winsock_server() ioctlsocket() failed: " << ret << std::endl;
      }

      m_client_sockets.push_back(client_socket);
    }
    else
    {
      int err = WSAGetLastError();
      switch(err)
      {
        case WSAEWOULDBLOCK:
          break;

        default:
          m_out << "error: accept() failed:" << err << std::endl;
          closesocket(m_listen_socket);
          m_listen_socket = INVALID_SOCKET;
          break;
      }
    }
  }
}

void
rFactorLCDPlugin::update_winsock_clients()
{
  m_out << "update winsock clients: " << m_client_sockets.size() << std::endl;
  bool needs_cleanup = false;

  for(std::vector<SOCKET>::iterator sock_it = m_client_sockets.begin();
      sock_it != m_client_sockets.end();
      ++sock_it)
  {
    if (*sock_it != INVALID_SOCKET)
    {
      char recvbuf[1024];

      int ret = recv(*sock_it, recvbuf, sizeof(recvbuf), 0);
      if (ret > 0)
      {
        m_out << "bytes received:" << ret << std::endl;

        if (false) // echo server
        {
          ret = send(*sock_it, recvbuf, ret, 0);
          if (ret == SOCKET_ERROR)
          {
            m_out << "send failed:" << WSAGetLastError() << std::endl;
            closesocket(*sock_it);
            *sock_it = INVALID_SOCKET;
            needs_cleanup = true;
          }
          m_out << "Bytes sent:" << ret << std::endl;
        }
      }
      else if (ret == 0)
      {
        m_out << "Connection closing..." << std::endl;
        closesocket(*sock_it);
        *sock_it = INVALID_SOCKET;
        needs_cleanup = true;
      }
      else
      {
        int err = WSAGetLastError();
        if (err != WSAEWOULDBLOCK)
        {
          m_out << "recv failed:" << err << std::endl;
          closesocket(*sock_it);
          *sock_it = INVALID_SOCKET;
          needs_cleanup = true;
        }
      }
    }
  }

  m_out << "update winsock clients: cleanup" << std::endl;
  if (needs_cleanup)
  {
    m_client_sockets.erase(std::remove(m_client_sockets.begin(), m_client_sockets.end(),
                                       INVALID_SOCKET),
                           m_client_sockets.end());
  }
}

void
rFactorLCDPlugin::send_message(const NetworkMessage& msg)
{
  for(std::vector<SOCKET>::iterator sock_it = m_client_sockets.begin();
      sock_it != m_client_sockets.end();
      ++sock_it)
  {
    if (*sock_it != INVALID_SOCKET)
    {
      int ret = send(*sock_it, msg.get_data(), msg.get_size(), 0);
      if (ret == SOCKET_ERROR)
      {
        m_out << "send failed:" << WSAGetLastError() << std::endl;
        closesocket(*sock_it);
        *sock_it = INVALID_SOCKET;
      }
    }
  }
}

void
rFactorLCDPlugin::shutdown_winsock()
{
  m_out << "shutdown winsock" << std::endl;
  WSACleanup();
}

void
rFactorLCDPlugin::Startup()
{
  m_out << "startup" << std::endl;
  setup_winsock();
}

void
rFactorLCDPlugin::Shutdown()
{
  m_out << "shutdown" << std::endl;
  shutdown_winsock();
}

void
rFactorLCDPlugin::EnterRealtime()
{
  m_out << "enter_realtime" << std::endl;

  NetworkMessage msg(START_REALTIME_TAG);
  send_message(msg);
}

void
rFactorLCDPlugin::ExitRealtime()
{
  m_out << "exit_realtime" << std::endl;

  NetworkMessage msg(END_REALTIME_TAG);
  send_message(msg);
}

void
rFactorLCDPlugin::StartSession()
{
  m_out << "start_session" << std::endl;

  NetworkMessage msg(START_SESSION_TAG);
  send_message(msg);
}

void
rFactorLCDPlugin::EndSession()
{
  m_out << "end_session" << std::endl;

  NetworkMessage msg(END_SESSION_TAG);
  send_message(msg);
}

void
rFactorLCDPlugin::UpdateTelemetry(const TelemInfoV2& info)
{
  //m_out << "telemetry" << std::endl;
  update_winsock();

  NetworkMessage msg(TELEMETRY_TAG);
  msg.write_int(info.mGear);
  msg.write_float(info.mEngineRPM);
  msg.write_float(info.mEngineMaxRPM);
  msg.write_float(info.mClutchRPM);

  msg.write_float(info.mFuel);
  msg.write_float(info.mEngineWaterTemp);
  msg.write_float(info.mEngineOilTemp);

  msg.write_float(info.mUnfilteredThrottle);
  msg.write_float(info.mUnfilteredBrake);
  msg.write_float(info.mUnfilteredSteering);
  msg.write_float(info.mUnfilteredClutch);

  msg.write_float(info.mSteeringArmForce);

  for(int i = 0; i < 8; ++i)
  {
    msg.write_char(info.mDentSeverity[i]);
  }

  for(int i = 0; i < 4; ++i)
  {
    const TelemWheelV2& wheel = info.mWheel[i];
    msg.write_float(wheel.mRotation);
    msg.write_float(wheel.mSuspensionDeflection);
    msg.write_float(wheel.mRideHeight);
    msg.write_float(wheel.mTireLoad);
    msg.write_float(wheel.mLateralForce);
    msg.write_float(wheel.mGripFract);
    msg.write_float(wheel.mBrakeTemp);
    msg.write_float(wheel.mPressure);
    msg.write_float(wheel.mTemperature[0]);
    msg.write_float(wheel.mTemperature[1]);
    msg.write_float(wheel.mTemperature[2]);

    msg.write_float(wheel.mWear);
    msg.write_char(wheel.mSurfaceType);
    msg.write_char(wheel.mFlat);
    msg.write_char(wheel.mDetached);
  }
  send_message(msg);
}

void
rFactorLCDPlugin::UpdateScoring(const ScoringInfoV2& info)
{
  m_out << "scoring" << std::endl;

  {
    // data that should be constant across a session
    NetworkMessage msg(INFO_TAG);
    msg.write_string(info.mTrackName);
    msg.write_string(info.mPlayerName);
    msg.write_string(info.mPlrFileName);
    msg.write_float(info.mEndET);
    msg.write_int(info.mMaxLaps);
    msg.write_float(info.mLapDist);
    msg.write_float(info.mNumVehicles);
    send_message(msg);
  }
  {
    // data that varies
    NetworkMessage msg(SCORE_TAG);
    msg.write_char(info.mGamePhase);
    msg.write_char(info.mYellowFlagState);
    msg.write_char(info.mSectorFlag[0]);
    msg.write_char(info.mSectorFlag[1]);
    msg.write_char(info.mSectorFlag[2]);
    msg.write_char(info.mStartLight);
    msg.write_char(info.mNumRedLights);
    msg.write_int(info.mSession);
    msg.write_float(info.mCurrentET);
    msg.write_float(info.mAmbientTemp);
    msg.write_float(info.mTrackTemp);
    send_message(msg);
  }
  {
    // per vehicle data
    NetworkMessage msg(VEHICLE_TAG);
    for(int i = 0; i < info.mNumVehicles; ++i)
    {
      VehicleScoringInfoV2& veh = info.mVehicle[i];

      msg.write_char(veh.mIsPlayer);
      msg.write_string(veh.mDriverName);
      msg.write_string(veh.mVehicleName);
      msg.write_string(veh.mVehicleClass);
      msg.write_short(veh.mTotalLaps);

      msg.write_char(veh.mInPits);
      msg.write_char(veh.mPlace);
      msg.write_float(veh.mTimeBehindNext);
      msg.write_int(veh.mLapsBehindNext);
      msg.write_float(veh.mTimeBehindLeader);
      msg.write_int(veh.mLapsBehindLeader);

      msg.write_float(veh.mBestSector1);
      msg.write_float(veh.mBestSector2);
      msg.write_float(veh.mBestLapTime);
      msg.write_float(veh.mLastSector1);
      msg.write_float(veh.mLastSector2);
      msg.write_float(veh.mLastLapTime);
      msg.write_float(veh.mCurSector1);
      msg.write_float(veh.mCurSector2);

      msg.write_short(veh.mNumPitstops);
      msg.write_short(veh.mNumPenalties);

      msg.write_int(veh.mLapStartET);
    }
    send_message(msg);
  }
  m_out << "scoring sending mgs done" << std::endl;

  update_winsock();
  m_out << "scoring update winsock done" << std::endl;
}

/* EOF */
