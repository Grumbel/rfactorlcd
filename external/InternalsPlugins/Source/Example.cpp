//‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹‹
//›                                                                         ﬁ
//› Module: Internals Example Source File                                   ﬁ
//›                                                                         ﬁ
//› Description: Declarations for the Internals Example Plugin              ﬁ
//›                                                                         ﬁ
//›                                                                         ﬁ
//› This source code module, and all information, data, and algorithms      ﬁ
//› associated with it, are part of CUBE technology (tm).                   ﬁ
//›                 PROPRIETARY AND CONFIDENTIAL                            ﬁ
//› Copyright (c) 1996-2007 Image Space Incorporated.  All rights reserved. ﬁ
//›                                                                         ﬁ
//›                                                                         ﬁ
//› Change history:                                                         ﬁ
//›   tag.2005.11.30: created                                               ﬁ
//›                                                                         ﬁ
//ﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂﬂ

#include "Example.hpp"          // corresponding header file
#include <math.h>               // for atan2, sqrt
#include <stdio.h>              // for sample output


// plugin information
unsigned g_uPluginID          = 0;
char     g_szPluginName[]     = "ExampleInternalsPlugin - 2005.11.30";
unsigned g_uPluginVersion     = 001;
unsigned g_uPluginObjectCount = 1;
InternalsPluginInfo g_PluginInfo;

// interface to plugin information
extern "C" __declspec(dllexport)
const char* __cdecl GetPluginName() { return g_szPluginName; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginVersion() { return g_uPluginVersion; }

extern "C" __declspec(dllexport)
unsigned __cdecl GetPluginObjectCount() { return g_uPluginObjectCount; }

// get the plugin-info object used to create the plugin.
extern "C" __declspec(dllexport)
PluginObjectInfo* __cdecl GetPluginObjectInfo( const unsigned uIndex )
{
  switch(uIndex)
  {
    case 0:
      return  &g_PluginInfo;
    default:
      return 0;
  }
}


// InternalsPluginInfo class

InternalsPluginInfo::InternalsPluginInfo()
{
  // put together a name for this plugin
  sprintf( m_szFullName, "%s - %s", g_szPluginName, InternalsPluginInfo::GetName() );
}

const char*    InternalsPluginInfo::GetName()     const { return ExampleInternalsPlugin::GetName(); }
const char*    InternalsPluginInfo::GetFullName() const { return m_szFullName; }
const char*    InternalsPluginInfo::GetDesc()     const { return "Example Internals Plugin"; }
const unsigned InternalsPluginInfo::GetType()     const { return ExampleInternalsPlugin::GetType(); }
const char*    InternalsPluginInfo::GetSubType()  const { return ExampleInternalsPlugin::GetSubType(); }
const unsigned InternalsPluginInfo::GetVersion()  const { return ExampleInternalsPlugin::GetVersion(); }
void*          InternalsPluginInfo::Create()      const { return new ExampleInternalsPlugin(); }


// InternalsPlugin class

const char ExampleInternalsPlugin::m_szName[] = "InternalsPlugin";
const char ExampleInternalsPlugin::m_szSubType[] = "Internals";
const unsigned ExampleInternalsPlugin::m_uID = 1;
const unsigned ExampleInternalsPlugin::m_uVersion = 3;  // set to 3 for InternalsPluginV3 functionality and added graphical and vehicle info


PluginObjectInfo *ExampleInternalsPlugin::GetInfo()
{
  return &g_PluginInfo;
}


void ExampleInternalsPlugin::WriteToAllExampleOutputFiles( const char * const openStr, const char * const msg )
{
  FILE *fo;

  fo = fopen( "ExampleInternalsTelemetryOutput.txt", openStr );
  if( fo != NULL )
  {
    fprintf( fo, "%s\n", msg );
    fclose( fo );
  }

  fo = fopen( "ExampleInternalsGraphicsOutput.txt", openStr );
  if( fo != NULL )
  {
    fprintf( fo, "%s\n", msg );
    fclose( fo );
  }

  fo = fopen( "ExampleInternalsScoringOutput.txt", openStr );
  if( fo != NULL )
  {
    fprintf( fo, "%s\n", msg );
    fclose( fo );
  }
}


void ExampleInternalsPlugin::Startup()
{
  // Open ports, read configs, whatever you need to do.  For now, I'll just clear out the
  // example output data files.
  WriteToAllExampleOutputFiles( "w", "-STARTUP-" );

  // default HW control enabled to true
  mEnabled = true;
}


void ExampleInternalsPlugin::Shutdown()
{
  WriteToAllExampleOutputFiles( "a", "-SHUTDOWN-" );
}


void ExampleInternalsPlugin::StartSession()
{
  WriteToAllExampleOutputFiles( "a", "--STARTSESSION--" );
}


void ExampleInternalsPlugin::EndSession()
{
  WriteToAllExampleOutputFiles( "a", "--ENDSESSION--" );
}


void ExampleInternalsPlugin::EnterRealtime()
{
  // start up timer every time we enter realtime
  mET = 0.0f;
  WriteToAllExampleOutputFiles( "a", "---ENTERREALTIME---" );
}


void ExampleInternalsPlugin::ExitRealtime()
{
  WriteToAllExampleOutputFiles( "a", "---EXITREALTIME---" );
}


void ExampleInternalsPlugin::UpdateTelemetry( const TelemInfoV2 &info )
{
  // Use the incoming data, for now I'll just write some of it to a file to a) make sure it
  // is working, and b) explain the coordinate system a little bit (see header for more info)
  FILE *fo = fopen( "ExampleInternalsTelemetryOutput.txt", "a" );
  if( fo != NULL )
  {
    // Delta time is variable, as we send out the info once per frame
    fprintf( fo, "DT=%.4f\n", info.mDeltaTime );
    fprintf( fo, "Lap=%d StartET=%.3f\n", info.mLapNumber, info.mLapStartET );
    fprintf( fo, "Vehicle=%s\n", info.mVehicleName );
    fprintf( fo, "Track=%s\n", info.mTrackName );
    fprintf( fo, "Pos=(%.3f,%.3f,%.3f)\n", info.mPos.x, info.mPos.y, info.mPos.z );

    // Forward is roughly in the -z direction (although current pitch of car may cause some y-direction velocity)
    fprintf( fo, "LocalVel=(%.2f,%.2f,%.2f)\n", info.mLocalVel.x, info.mLocalVel.y, info.mLocalVel.z );
    fprintf( fo, "LocalAccel=(%.1f,%.1f,%.1f)\n", info.mLocalAccel.x, info.mLocalAccel.y, info.mLocalAccel.z );

    // Orientation matrix is left-handed
    fprintf( fo, "[%6.3f,%6.3f,%6.3f]\n", info.mOriX.x, info.mOriX.y, info.mOriX.z );
    fprintf( fo, "[%6.3f,%6.3f,%6.3f]\n", info.mOriY.x, info.mOriY.y, info.mOriY.z );
    fprintf( fo, "[%6.3f,%6.3f,%6.3f]\n", info.mOriZ.x, info.mOriZ.y, info.mOriZ.z );
    fprintf( fo, "LocalRot=(%.3f,%.3f,%.3f)\n", info.mLocalRot.x, info.mLocalRot.y, info.mLocalRot.z );
    fprintf( fo, "LocalRotAccel=(%.2f,%.2f,%.2f)\n", info.mLocalRotAccel.x, info.mLocalRotAccel.y, info.mLocalRotAccel.z );

    // Vehicle status
    fprintf( fo, "Gear=%d RPM=%.1f RevLimit=%.1f\n", info.mGear, info.mEngineRPM, info.mEngineMaxRPM );
    fprintf( fo, "Water=%.1f Oil=%.1f\n", info.mEngineWaterTemp, info.mEngineOilTemp );
    fprintf( fo, "ClutchRPM=%.1f\n", info.mClutchRPM );

    // Driver input
    fprintf( fo, "UnfilteredThrottle=%.1f%%\n", 100.0f * info.mUnfilteredThrottle );
    fprintf( fo, "UnfilteredBrake=%.1f%%\n", 100.0f * info.mUnfilteredBrake );
    fprintf( fo, "UnfilteredSteering=%.1f%%\n", 100.0f * info.mUnfilteredSteering );
    fprintf( fo, "UnfilteredClutch=%.1f%%\n", 100.0f * info.mUnfilteredClutch );

    // Misc
    fprintf( fo, "SteeringArmForce=%.1f\n", info.mSteeringArmForce );
    fprintf( fo, "Fuel=%.1f ScheduledStops=%d Overheating=%d Detached=%d\n", info.mFuel, info.mScheduledStops, info.mOverheating, info.mDetached );
    fprintf( fo, "Dents=(%d,%d,%d,%d,%d,%d,%d,%d)\n", info.mDentSeverity[0], info.mDentSeverity[1], info.mDentSeverity[2], info.mDentSeverity[3],
                                                      info.mDentSeverity[4], info.mDentSeverity[5], info.mDentSeverity[6], info.mDentSeverity[7] );
    fprintf( fo, "LastImpactET=%.1f Mag=%.1f, Pos=(%.1f,%.1f,%.1f)\n", info.mLastImpactET, info.mLastImpactMagnitude,
             info.mLastImpactPos.x, info.mLastImpactPos.y, info.mLastImpactPos.z );

    // Wheels
    for( long i = 0; i < 4; ++i )
    {
      const TelemWheelV2 &wheel = info.mWheel[i];
      fprintf( fo, "Wheel=%s\n", (i==0)?"FrontLeft":(i==1)?"FrontRight":(i==2)?"RearLeft":"RearRight" );
      fprintf( fo, " ForwardRotation=%.1f\n", -wheel.mRotation );
      fprintf( fo, " SuspensionDeflection=%.3f RideHeight=%.3f\n", wheel.mSuspensionDeflection, wheel.mRideHeight );
      fprintf( fo, " TireLoad=%.1f LateralForce=%.1f GripFract=%.3f\n", wheel.mTireLoad, wheel.mLateralForce, wheel.mGripFract );
      fprintf( fo, " BrakeTemp=%.1f TirePressure=%.1f\n", wheel.mBrakeTemp, wheel.mPressure );
      fprintf( fo, " TireTemp(l/c/r)=%.1f/%.1f/%.1f\n", wheel.mTemperature[0], wheel.mTemperature[1], wheel.mTemperature[2] );
      fprintf( fo, " Wear=%.3f TerrainName=%s SurfaceType=%d\n", wheel.mWear, wheel.mTerrainName, wheel.mSurfaceType );
      fprintf( fo, " Flat=%d Detached=%d\n", wheel.mFlat, wheel.mDetached );
    }

    // Compute some auxiliary info based on the above
    TelemVect3 forwardVector = { -info.mOriX.z, -info.mOriY.z, -info.mOriZ.z };
    TelemVect3    leftVector = {  info.mOriX.x,  info.mOriY.x,  info.mOriZ.x };

    // These are normalized vectors, and remember that our world Y coordinate is up.  So you can
    // determine the current pitch and roll (w.r.t. the world x-z plane) as follows:
    const float pitch = atan2f( forwardVector.y, sqrtf( ( forwardVector.x * forwardVector.x ) + ( forwardVector.z * forwardVector.z ) ) );
    const float  roll = atan2f(    leftVector.y, sqrtf( (    leftVector.x *    leftVector.x ) + (    leftVector.z *    leftVector.z ) ) );
    const float radsToDeg = 57.296f;
    fprintf( fo, "Pitch = %.1f deg, Roll = %.1f deg\n", pitch * radsToDeg, roll * radsToDeg );

    const float metersPerSec = sqrtf( ( info.mLocalVel.x * info.mLocalVel.x ) +
                                      ( info.mLocalVel.y * info.mLocalVel.y ) +
                                      ( info.mLocalVel.z * info.mLocalVel.z ) );
    fprintf( fo, "Speed = %.1f KPH, %.1f MPH\n\n", metersPerSec * 3.6f, metersPerSec * 2.237f );

    // Close file
    fclose( fo );
  }
}


void ExampleInternalsPlugin::UpdateGraphics( const GraphicsInfoV2 &info )
{
  // Use the incoming data, for now I'll just write some of it to a file to a) make sure it
  // is working, and b) explain the coordinate system a little bit (see header for more info)
  FILE *fo = fopen( "ExampleInternalsGraphicsOutput.txt", "a" );
  if( fo != NULL )
  {
    // Print stuff
    fprintf( fo, "CamPos=(%.1f,%.1f,%.1f)\n", info.mCamPos.x, info.mCamPos.y, info.mCamPos.z );
    fprintf( fo, "CamOri=(%.1f,%.1f,%.1f)\n", info.mCamOri.x, info.mCamOri.y, info.mCamOri.z );
    fprintf( fo, "HWND=%d\n", info.mHWND );
    fprintf( fo, "Ambient Color=(%.1f,%.1f,%.1f)\n\n", info.mAmbientRed, info.mAmbientGreen, info.mAmbientBlue );

    // Close file
    fclose( fo );
  }
}


bool ExampleInternalsPlugin::CheckHWControl( const char * const controlName, float &fRetVal )
{
  // only if enabled, of course
  if( !mEnabled )
    return( false );

  // Note that incoming value is the game's computation, in case you're interested.

  // Sorry, no control allowed over actual vehicle inputs ... would be too easy to cheat!
  // However, you can still look at the values.

  // Note: since the game calls this function every frame for every available control, you might consider
  // doing a binary search if you are checking more than 7 or 8 strings, just to keep the speed up.
  if( _stricmp( controlName, "LookLeft" ) == 0 )
  {
    const float headSwitcheroo = fmodf( mET, 2.0f );
    if( headSwitcheroo < 0.5 )
      fRetVal = 1.0f;
    else
      fRetVal = 0.0f;
    return( true );
  }
  else if( _stricmp( controlName, "LookRight" ) == 0 )
  {
    const float headSwitcheroo = fmodf( mET, 2.0f );
    if( ( headSwitcheroo > 1.0f ) && ( headSwitcheroo < 1.5f ) )
      fRetVal = 1.0f;
    else
      fRetVal = 0.0f;
    return( true );
  }

  return( false );
}


bool ExampleInternalsPlugin::ForceFeedback( float &forceValue )
{
  // Note that incoming value is the game's computation, in case you're interested.

  // CHANGE COMMENTS TO ENABLE FORCE EXAMPLE
  return( false );

  // I think the bounds are -11500 to 11500 ...
//  forceValue = 11500.0f * sinf( mET );
//  return( true );
}


void ExampleInternalsPlugin::UpdateScoring( const ScoringInfoV2 &info )
{
  // Note: function is called twice per second now (instead of once per second in previous versions)
  FILE *fo = fopen( "ExampleInternalsScoringOutput.txt", "a" );
  if( fo != NULL )
  {
    // Print general scoring info
    fprintf( fo, "TrackName=%s\n", info.mTrackName );
    fprintf( fo, "Session=%d NumVehicles=%d CurET=%.3f\n", info.mSession, info.mNumVehicles, info.mCurrentET );
    fprintf( fo, "EndET=%.3f MaxLaps=%d LapDist=%.1f\n", info.mEndET, info.mMaxLaps, info.mLapDist );

    // Note that only one plugin can use the stream (by enabling scoring updates) ... sorry if any clashes result
    fprintf( fo, "START STREAM\n" );
    const char *ptr = info.mResultsStream;
    while( *ptr != NULL )
      fputc( *ptr++, fo );
    fprintf( fo, "END STREAM\n" );

    // New version 2 stuff
    fprintf( fo, "GamePhase=%d YellowFlagState=%d SectorFlags=(%d,%d,%d)\n", info.mGamePhase, info.mYellowFlagState,
             info.mSectorFlag[0], info.mSectorFlag[1], info.mSectorFlag[2] );
    fprintf( fo, "InRealtime=%d StartLight=%d NumRedLights=%d\n", info.mInRealtime, info.mStartLight, info.mNumRedLights );
    fprintf( fo, "PlayerName=%s PlrFileName=%s\n", info.mPlayerName, info.mPlrFileName );
    fprintf( fo, "DarkCloud=%.2f Raining=%.2f AmbientTemp=%.1f TrackTemp=%.1f\n", info.mDarkCloud, info.mRaining, info.mAmbientTemp, info.mTrackTemp );
    fprintf( fo, "Wind=(%.1f,%.1f,%.1f) OnPathWetness=%.2f OffPathWetness=%.2f\n", info.mWind.x, info.mWind.y, info.mWind.z, info.mOnPathWetness, info.mOffPathWetness );

    // Print vehicle info
    for( long i = 0; i < info.mNumVehicles; ++i )
    {
      VehicleScoringInfoV2 &vinfo = info.mVehicle[ i ];
      fprintf( fo, "Driver %d: %s\n", i, vinfo.mDriverName );
      fprintf( fo, " Vehicle=%s\n", vinfo.mVehicleName );
      fprintf( fo, " Laps=%d Sector=%d FinishStatus=%d\n", vinfo.mTotalLaps, vinfo.mSector, vinfo.mFinishStatus );
      fprintf( fo, " LapDist=%.1f PathLat=%.2f RelevantTrackEdge=%.2f\n", vinfo.mLapDist, vinfo.mPathLateral, vinfo.mTrackEdge );
      fprintf( fo, " Best=(%.3f, %.3f, %.3f)\n", vinfo.mBestSector1, vinfo.mBestSector2, vinfo.mBestLapTime );
      fprintf( fo, " Last=(%.3f, %.3f, %.3f)\n", vinfo.mLastSector1, vinfo.mLastSector2, vinfo.mLastLapTime );
      fprintf( fo, " Current Sector 1 = %.3f, Current Sector 2 = %.3f\n", vinfo.mCurSector1, vinfo.mCurSector2 );
      fprintf( fo, " Pitstops=%d, Penalties=%d\n", vinfo.mNumPitstops, vinfo.mNumPenalties );

      // New version 2 stuff
      fprintf( fo, " IsPlayer=%d Control=%d InPits=%d LapStartET=%.3f\n", vinfo.mIsPlayer, vinfo.mControl, vinfo.mInPits, vinfo.mLapStartET );
      fprintf( fo, " Place=%d VehicleClass=%s\n", vinfo.mPlace, vinfo.mVehicleClass );
      fprintf( fo, " TimeBehindNext=%.3f LapsBehindNext=%d\n", vinfo.mTimeBehindNext, vinfo.mLapsBehindNext );
      fprintf( fo, " TimeBehindLeader=%.3f LapsBehindLeader=%d\n", vinfo.mTimeBehindLeader, vinfo.mLapsBehindLeader );
      fprintf( fo, " Pos=(%.3f,%.3f,%.3f)\n", vinfo.mPos.x, vinfo.mPos.y, vinfo.mPos.z );

      // Forward is roughly in the -z direction (although current pitch of car may cause some y-direction velocity)
      fprintf( fo, " LocalVel=(%.2f,%.2f,%.2f)\n", vinfo.mLocalVel.x, vinfo.mLocalVel.y, vinfo.mLocalVel.z );
      fprintf( fo, " LocalAccel=(%.1f,%.1f,%.1f)\n", vinfo.mLocalAccel.x, vinfo.mLocalAccel.y, vinfo.mLocalAccel.z );

      // Orientation matrix is left-handed
      fprintf( fo, " [%6.3f,%6.3f,%6.3f]\n", vinfo.mOriX.x, vinfo.mOriX.y, vinfo.mOriX.z );
      fprintf( fo, " [%6.3f,%6.3f,%6.3f]\n", vinfo.mOriY.x, vinfo.mOriY.y, vinfo.mOriY.z );
      fprintf( fo, " [%6.3f,%6.3f,%6.3f]\n", vinfo.mOriZ.x, vinfo.mOriZ.y, vinfo.mOriZ.z );
      fprintf( fo, " LocalRot=(%.3f,%.3f,%.3f)\n", vinfo.mLocalRot.x, vinfo.mLocalRot.y, vinfo.mLocalRot.z );
      fprintf( fo, " LocalRotAccel=(%.2f,%.2f,%.2f)\n", vinfo.mLocalRotAccel.x, vinfo.mLocalRotAccel.y, vinfo.mLocalRotAccel.z );
    }
      
    // Delimit sections
    fprintf( fo, "\n" );

    // Close file
    fclose( fo );
  }
}


bool ExampleInternalsPlugin::RequestCommentary( CommentaryRequestInfo &info )
{
  // COMMENT OUT TO ENABLE EXAMPLE
  return( false );

  // only if enabled, of course
  if( !mEnabled )
    return( false );

  // Note: function is called twice per second

  // Say green flag event for no particular reason every 20 seconds ...
  const float timeMod20 = fmodf( mET, 20.0f );
  if( timeMod20 > 19.0f )
  {
    strcpy( info.mName, "GreenFlag" );
    info.mInput1 = 0.0f;
    info.mInput2 = 0.0f;
    info.mInput3 = 0.0f;
    info.mSkipChecks = true;
    return( true );
  }

  return( false );
}

