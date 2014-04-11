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


InternalsPluginInfo g_PluginInfo;


// interface to plugin information
extern "C" __declspec(dllexport)
const char* __cdecl GetPluginName() { return "rfactorlcdPlugin 0.0.0"; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginVersion() { return 1; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginObjectCount() { return 1; }

extern "C" __declspec(dllexport)
PluginObjectInfo* __cdecl GetPluginObjectInfo( const unsigned uIndex )
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


rFactorLCDPlugin::rFactorLCDPlugin() :
  m_out("C:\\rfactor_plugin.txt")
{
}

rFactorLCDPlugin::~rFactorLCDPlugin()
{  
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
rFactorLCDPlugin::Startup()
{
  m_out << "startup" << std::endl;
}

void
rFactorLCDPlugin::Shutdown()
{
  m_out << "shutdown" << std::endl;
}

void
rFactorLCDPlugin::EnterRealtime()
{
  m_out << "enter_realtime" << std::endl;
}

void
rFactorLCDPlugin::ExitRealtime()
{
  m_out << "exit_realtime" << std::endl;
}

void
rFactorLCDPlugin::StartSession()
{
  m_out << "start_session" << std::endl;
}

void
rFactorLCDPlugin::EndSession()
{
  m_out << "end_session" << std::endl;
}

/* EOF */
