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


#ifndef HEADER_RFACTORLCD_HPP
#define HEADER_RFACTORLCD_HPP

#define WINVER 0x501
#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>

#include <vector>
#include <fstream>

#include "InternalsPlugin.hpp"


class rFactorLCDPlugin : public InternalsPluginV3
{
private:
  std::ofstream m_out;
  SOCKET m_listen_socket;
  std::vector<SOCKET> m_client_sockets;
  
public:
  rFactorLCDPlugin();
  virtual ~rFactorLCDPlugin();

  virtual PluginObjectInfo* GetInfo();
  virtual unsigned int GetPropertyCount() const { return 0; }
  virtual PluginObjectProperty* GetProperty(unsigned int) { return 0; }
  virtual PluginObjectProperty* GetProperty(const char*) { return 0; }

  /** Called once when the plugin is initialized */
  virtual void Startup();

  /** Called once when the plugin is shutdown */
  virtual void Shutdown();

  /** Called once after Shutdown() */
  virtual void Destroy();

  /** Called when the player enters the track */
  virtual void EnterRealtime();

  /** Called when the player leaves the track */
  virtual void ExitRealtime();

  /** Called whenever a session is started, race sessions can be ended
      and restarted while in Realtime (i.e. pressing the restart-race
      keyboard shortcut) */
  virtual void StartSession();

  /** Called when a session has ended */
  virtual void EndSession();

  /** Called with new telemetry data ~90 times a second */
  virtual void UpdateTelemetry( const TelemInfoV2 &info );
  virtual bool WantsTelemetryUpdates() { return true; }

  /** Called with new scoring data twice per second */
  virtual void UpdateScoring(const ScoringInfoV2& info);
  virtual bool WantsScoringUpdates() { return true; }

  void setup_winsock();
  void update_winsock();
  void update_winsock_server();
  void update_winsock_clients();
  void shutdown_winsock();

private:
  rFactorLCDPlugin(const rFactorLCDPlugin&);
  rFactorLCDPlugin& operator=(const rFactorLCDPlugin&);
};


class InternalsPluginInfo : public PluginObjectInfo
{
public:
  InternalsPluginInfo() {}
  ~InternalsPluginInfo() {}

  virtual const char*    GetName()     const { return "rFactorLCDPlugin"; }
  virtual const char*    GetFullName() const { return "rFactorLCDPlugin - InternalsPlugin"; }
  virtual const char*    GetDesc()     const { return "rFactorLCDPlugin for Remote Access"; }
  virtual const unsigned GetType()     const { return PO_INTERNALS; }
  virtual const char*    GetSubType()  const { return "Internals"; }
  virtual const unsigned GetVersion()  const { return 3; }
  virtual void*          Create()      const { return new rFactorLCDPlugin(); }
};


#endif

/* EOF */
