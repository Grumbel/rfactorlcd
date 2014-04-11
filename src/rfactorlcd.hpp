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


#include <fstream>

#include "InternalsPlugin.hpp"


class rFactorLCDPlugin : public InternalsPluginV3
{
private:
  std::ofstream m_out;
  
public:
  rFactorLCDPlugin();
  virtual ~rFactorLCDPlugin();
  
  virtual void Destroy();
  virtual PluginObjectInfo* GetInfo();
  virtual unsigned int GetPropertyCount() const { return 0; }
  virtual PluginObjectProperty* GetProperty(unsigned int) { return 0; }
  virtual PluginObjectProperty* GetProperty(const char*) { return 0; }

  void Startup();
  void Shutdown();

  void EnterRealtime();
  void ExitRealtime();

  void StartSession();
  void EndSession();
  
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
