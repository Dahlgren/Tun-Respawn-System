#define COMPONENT msp
#define PREFIX Tun

#define MAJOR 1
#define MINOR 6
#define PATCHLVL 3
#define BUILD 06052022

#define VERSION MAJOR.MINOR.PATCHLVL.BUILD
#define VERSION_AR MAJOR,MINOR,PATCHLVL,BUILD

// MINIMAL required version for the Mod. Components can specify others..
#define REQUIRED_VERSION 2.06

#define DEBUG_MODE_FULL

#include "\x\cba\addons\main\script_macros_common.hpp"

// Default versioning level
#define DEFAULT_VERSIONING_LEVEL 2

//AAR update macro
#define AAR_UPDATE(OBJ,VARNAME,VALUE) if ( !isnil "afi_aar2" ) then { [OBJ, VARNAME, VALUE] call afi_aar2_fnc_addcustomdata; };