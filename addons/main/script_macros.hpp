#include "\z\ace\addons\main\script_macros.hpp"

#ifdef DISABLE_COMPILE_CACHE
    #undef PREP
    #define PREP(fncName) DFUNC(fncName) = compile preprocessFileLineNumbers QPATHTOF(functions\DOUBLES(fnc,fncName).sqf)
#else
    #undef PREP
    #define PREP(fncName) [QPATHTOF(functions\DOUBLES(fnc,fncName).sqf), QFUNC(fncName)] call CBA_fnc_compileFunction
#endif

//
#define MARKER_NAME_CONFIG(var1) QUOTE(DOUBLES(ADDON,var1))

#define MARKER_NAME(var1) FORMAT_2("%1_%2",QUOTE(ADDON),var1)

//AAR enabled check
#define AAR_IS_ENABLED !isNil "afi_aar2"
//AAR update macro
#define AAR_UPDATE(OBJ,VARNAME,VALUE)   [QEGVAR(main,AAR_UpdateEH), [OBJ,VARNAME,VALUE]] call CBA_fnc_serverEvent
//AAR event
#define AAR_EVENT(TEXT,INSTIGATOR,TARGET,POI)   [QEGVAR(main,AAR_EventEH), [TEXT,INSTIGATOR,TARGET,POI]] call CBA_fnc_serverEvent


#define ALL_SIDES   [west,east,resistance,civilian]

//Hash template macros
#define EMPTY_ARRAY_FOR_SIDES [[west,[]],[east,[]],[resistance,[]],[civilian,[]]]
#define ZEROS_FOR_SIDES [[west,0],[east,0],[resistance,0],[civilian,0]]
#define FALSES_FOR_SIDES [[west,false],[east,false],[resistance,false],[civilian,false]]
#define TRUES_FOR_SIDES [[west,true],[east,true],[resistance,true],[civilian,true]]

//Spectator modes
#define MODE_FREE   0
#define MODE_FPS    1
#define MODE_FOLLOW 2
#define ALL_MODES   [MODE_FREE,MODE_FPS,MODE_FOLLOW]