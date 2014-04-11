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

// Need to link with Ws2_32.lib
#pragma comment(lib, "ws2_32.lib")


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

rFactorLCDPlugin::rFactorLCDPlugin() :
  m_out("C:\\rfactor_plugin.txt"),
  m_listen_socket(INVALID_SOCKET)
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
    const char* DEFAULT_PORT = "2909";

    struct addrinfo hints;
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    struct addrinfo* result_info = NULL;
    ret = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result_info);
    if (ret != 0)
    {
      m_out << "error: getaddrinfo failed: " << ret << std::endl;
      WSACleanup();
      return;
    }

    m_listen_socket = socket(result_info->ai_family, result_info->ai_socktype, result_info->ai_protocol);
    if (m_listen_socket == INVALID_SOCKET)
    {
      m_out << "Error at socket(): " << WSAGetLastError() << std::endl;
      freeaddrinfo(result_info);
      WSACleanup();
      return;
    }

    ret = bind(m_listen_socket, result_info->ai_addr, (int)result_info->ai_addrlen);
    if (ret == SOCKET_ERROR)
    {
      m_out << "bind failed with error: " << WSAGetLastError() << std::endl;
      freeaddrinfo(result_info);
      closesocket(m_listen_socket);
      WSACleanup();
      return;
    }

    if (listen(m_listen_socket, SOMAXCONN) == SOCKET_ERROR)
    {
      m_out << "Listen failed with error: " << WSAGetLastError() << std::endl;
      closesocket(m_listen_socket);
      WSACleanup();
      return;
    }

    // make m_listen_socket non-blocking
    u_long mode = 1;
    ret = ioctlsocket(m_listen_socket, FIONBIO, &mode);
    if (ret != 0)
    {
      m_out << "ioctlsocket() failed: " << ret << std::endl;
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
  // listen for incoming connections
  SOCKET client_socket = INVALID_SOCKET;
  client_socket = accept(m_listen_socket, NULL, NULL);
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
    if (err != WSAEWOULDBLOCK)
    {
      m_out << "error: accept() failed:" << err << std::endl;
      closesocket(m_listen_socket);
      WSACleanup();
      return;
    }
  }
}

void
rFactorLCDPlugin::update_winsock_clients()
{
  // check if any of the clients has send something

  int recvbuflen = 1024;
  char recvbuf[1024];
  int ret;
  int iSendResult;

  // Receive until the peer shuts down the connection
  for(std::vector<SOCKET>::iterator sock_it =  m_client_sockets.begin();
      sock_it != m_client_sockets.end();
      ++sock_it)
  {
    ret = recv(*sock_it, recvbuf, recvbuflen, 0);
    if (ret > 0)
    {
      m_out << "Bytes received:" << ret << std::endl;

      // Echo the buffer back to the sender
      iSendResult = send(*sock_it, recvbuf, ret, 0);
      if (iSendResult == SOCKET_ERROR)
      {
        m_out << "send failed:" << WSAGetLastError() << std::endl;
        closesocket(*sock_it);
        WSACleanup();
        return;
      }
      m_out << "Bytes sent:" << iSendResult << std::endl;
    }
    else if (ret == 0)
    {
      m_out << "Connection closing..." << std::endl;
    }
    else
    {
      m_out << "recv failed:" << WSAGetLastError() << std::endl;
      closesocket(*sock_it);
      WSACleanup();
      return;
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

  char buf[MAX_PATH];
  int bytes = GetModuleFileNameA(NULL, buf, MAX_PATH);
  if (bytes == 0)
  {
    m_out << "couldn't GetModuleFileNameA: " << GetLastError() << std::endl;
  }
  else
  {
    m_out << bytes << "   " << buf << std::endl;
  }

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

void
rFactorLCDPlugin::UpdateTelemetry(const TelemInfoV2& info)
{
  m_out << "telemetry" << std::endl;
  update_winsock();
}

void
rFactorLCDPlugin::UpdateScoring(const ScoringInfoV2& info)
{
  m_out << "scoring" << std::endl;
  update_winsock();
}

/* EOF */