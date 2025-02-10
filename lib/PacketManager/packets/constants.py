

MESSAGE_TYPES = [
    "FSNETCMD_NULL",                   #   0
    "FSNETCMD_LOGON",                  #   1 Cli ->Svr",  (Svr->Cli for log-on complete acknowledgement.)
    "FSNETCMD_LOGOFF",                 #   2
    "FSNETCMD_ERROR",                  #   3
    "FSNETCMD_LOADFIELD",              #   4 Svr ->Cli",   Cli->Svr for read back
    "FSNETCMD_ADDOBJECT",              #   5 Svr ->Cli
    "FSNETCMD_READBACK",               #   6 Svr<->Cli
    "FSNETCMD_SMOKECOLOR",             #   7 Svr<->Cli
    "FSNETCMD_JOINREQUEST",            #   8 Svr<- Cli
    "FSNETCMD_JOINAPPROVAL",           #   9 Svr ->Cli
    "FSNETCMD_REJECTJOINREQ",          #  10
    "FSNETCMD_AIRPLANESTATE",          #  11 Svr<->Cli   # Be careful in FsDeleteOldStatePacket when modify
    "FSNETCMD_UNJOIN",                 #  12 Svr<- Cli
    "FSNETCMD_REMOVEAIRPLANE",         #  13 Svr<->Cli
    "FSNETCMD_REQUESTTESTAIRPLANE",    #  14
    "FSNETCMD_KILLSERVER",             #  15 Svr<- Cli
    "FSNETCMD_PREPARESIMULATION",      #  16 Svr ->Cli
    "FSNETCMD_TESTPACKET",             #  17
    "FSNETCMD_LOCKON",                 #  18 Svr<->Cli
    "FSNETCMD_REMOVEGROUND",           #  19 Svr<->Cli
    "FSNETCMD_MISSILELAUNCH",          #  20 Svr<->Cli   # fsweapon.cpp is responsible for encoding/decoding
    "FSNETCMD_GROUNDSTATE",            #  21 Svr<->Cli   # Be careful in FsDeleteOldStatePacket when modify
    "FSNETCMD_GETDAMAGE",              #  22 Svr<->Cli
    "FSNETCMD_GNDTURRETSTATE",         #  23 Svr<->Cli
    "FSNETCMD_SETTESTAUTOPILOT",       #  24 Svr ->Cli
    "FSNETCMD_REQTOBESIDEWINDOWOFSVR", #  25 Svr<- Cli
    "FSNETCMD_ASSIGNSIDEWINDOW",       #  26 Svr ->Cli
    "FSNETCMD_RESENDAIRREQUEST",       #  27 Svr<- Cli
    "FSNETCMD_RESENDGNDREQUEST",       #  28 Svr<- Cli
    "FSNETCMD_VERSIONNOTIFY",          #  29 Svr ->Cli
    "FSNETCMD_AIRCMD",                 #  30 Svr<->Cli   # After 2001/06/24
    "FSNETCMD_USEMISSILE",             #  31 Svr ->Cli   # After 2001/06/24
    "FSNETCMD_TEXTMESSAGE",            #  32 Svr<->Cli
    "FSNETCMD_ENVIRONMENT",            #  33 Svr<->Cli  (*1)
    "FSNETCMD_NEEDRESENDJOINAPPROVAL", #  34 Svr<- Cli
    "FSNETCMD_REVIVEGROUND",           #  35 Svr ->Cli   # After 2004
    "FSNETCMD_WEAPONCONFIG",           #  36 Svr<->Cli   # After 20040618
    "FSNETCMD_LISTUSER",               #  37 Svr<->Cli   # After 20040726
    "FSNETCMD_QUERYAIRSTATE",          #  38 Cli ->Svr   # After 20050207
    "FSNETCMD_USEUNGUIDEDWEAPON",      #  39 Svr ->Cli   # After 20050323
    "FSNETCMD_AIRTURRETSTATE",         #  40 Svr<->Cli   # After 20050701
    "FSNETCMD_CTRLSHOWUSERNAME",       #  41 Svr ->Cli   # After 20050914
    "FSNETCMD_CONFIRMEXISTENCE",       #  42 Not Used
    "FSNETCMD_CONFIGSTRING",           #  43 Svr ->Cli   # After 20060514    Cli->Svr for read back
    "FSNETCMD_LIST",                   #  44 Svr ->Cli   # After 20060514    Cli->Svr for read back
    "FSNETCMD_GNDCMD",                 #  45 Svr<->Cli
    "FSNETCMD_REPORTSCORE",            #  46 Svr -> Cli  # After 20100630    (Older version will ignore)
    "FSNETCMD_SERVER_FORCE_JOIN",      #  47 Svr -> Cli
    "FSNETCMD_FOGCOLOR",               #  48 Svr -> Cli
    "FSNETCMD_SKYCOLOR",               #  49 Svr -> Cli
    "FSNETCMD_GNDCOLOR",               #  50 Svr -> Cli
    "FSNETCMD_RESERVED_FOR_LIGHTCOLOR",#  51 Svr -> Cli
    "FSNETCMD_GENERATEATTACKER",             #  52
    "FSNETCMD_RESERVED22",             #  53
    "FSNETCMD_RESERVED23",             #  54
    "FSNETCMD_RESERVED24",             #  55
    "FSNETCMD_RESERVED25",             #  56
    "FSNETCMD_RESERVED26",             #  57
    "FSNETCMD_RESERVED27",             #  58
    "FSNETCMD_RESERVED28",             #  59
    "FSNETCMD_RESERVED29",             #  60
    "FSNETCMD_RESERVED30",             #  61
    "FSNETCMD_RESERVED31",             #  62
    "FSNETCMD_RESERVED32",             #  63
    "FSNETCMD_OPENYSF_RESERVED33",     #  64 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED34",     #  65 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED35",     #  66 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED36",     #  67 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED37",     #  68 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED38",     #  69 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED39",     #  70 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED40",     #  71 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED41",     #  72 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED42",     #  73 Reserved for OpenYSF
    "FSNETCMD_RESERVED43",             #  74
    "FSNETCMD_RESERVED44",             #  75
    "FSNETCMD_RESERVED45",             #  76
    "FSNETCMD_RESERVED46",             #  77
    "FSNETCMD_RESERVED47",             #  78
    "FSNETCMD_RESERVED48",             #  79
    "FSNETCMD_RESERVED49",             #  80
    "FSNETCMD_NOP"
]

READBACKS = ["FSNETREADBACK_ADDAIRPLANE",
    "FSNETREADBACK_ADDGROUND",
    "FSNETREADBACK_REMOVEAIRPLANE",
    "FSNETREADBACK_REMOVEGROUND",
    "FSNETREADBACK_ENVIRONMENT",
    "FSNETREADBACK_JOINREQUEST",
    "FSNETREADBACK_JOINAPPROVAL",
    "FSNETREADBACK_PREPARE",
    "FSNETREADBACK____UNUSED____",
    "FSNETREADBACK_USEMISSILE",
    "FSNETREADBACK_USEUNGUIDEDWEAPON",
    "FSNETREADBACK_CTRLSHOWUSERNAME"]

FSWEAPON_DICT = {
    0: "FSWEAPON_GUN",
    1: "FSWEAPON_AIM9",
    2: "FSWEAPON_AGM65",
    3: "FSWEAPON_BOMB",
    4: "FSWEAPON_ROCKET",
    5: "FSWEAPON_FLARE",
    6: "FSWEAPON_AIM120",
    7: "FSWEAPON_BOMB250",
    8: "FSWEAPON_SMOKE",
    9: "FSWEAPON_BOMB500HD",
    10: "FSWEAPON_AIM9X",
    11: "FSWEAPON_FLAREPOD",
    12: "FSWEAPON_FUELTANK",
    13: "FSWEAPON_RESERVED13",
    14: "FSWEAPON_RESERVED14",
    15: "FSWEAPON_RESERVED15",
    16: "FSWEAPON_RESERVED16",
    17: "FSWEAPON_RESERVED17",
    18: "FSWEAPON_RESERVED18",
    19: "FSWEAPON_RESERVED19",
    20: "FSWEAPON_RESERVED20",
    21: "FSWEAPON_RESERVED21",
    22: "FSWEAPON_RESERVED22",
    23: "FSWEAPON_RESERVED23",
    24: "FSWEAPON_RESERVED24",
    25: "FSWEAPON_RESERVED25",
    26: "FSWEAPON_RESERVED26",
    27: "FSWEAPON_RESERVED27",
    28: "FSWEAPON_RESERVED28",
    29: "FSWEAPON_RESERVED29",
    30: "FSWEAPON_RESERVED30",
    31: "FSWEAPON_RESERVED31",
    32: "FSWEAPON_SMOKE0",
    33: "FSWEAPON_SMOKE1",
    34: "FSWEAPON_SMOKE2",
    35: "FSWEAPON_SMOKE3",
    36: "FSWEAPON_SMOKE4",
    37: "FSWEAPON_SMOKE5",
    38: "FSWEAPON_SMOKE6",
    39: "FSWEAPON_SMOKE7",
    40: "FSWEAPON_RESERVED40",
    41: "FSWEAPON_RESERVED41",
    42: "FSWEAPON_RESERVED42",
    43: "FSWEAPON_RESERVED43",
    44: "FSWEAPON_RESERVED44",
    45: "FSWEAPON_RESERVED45",
    46: "FSWEAPON_RESERVED46",
    47: "FSWEAPON_RESERVED47",
    48: "FSWEAPON_NUMWEAPONTYPE",
    127: "FSWEAPON_NULL",
    128: "FSWEAPON_DEBRIS",
    200: "FSWEAPON_FLARE_INTERNAL"
}

GUIDEDWEAPONS = missiles = ["FSWEAPON_AGM65", "FSWEAPON_AIM9", "FSWEAPON_AIM120",
                            "FSWEAPON_AIM9X", "FSWEAPON_ROCKET"]

ERROR_CODES = ["FSNETERR_NOERR",
	"FSNETERR_VERSIONCONFLICT",
	"FSNETERR_CANNOTADDOBJECT",
	"FSNETERR_REJECT",
	"FSNETERR_CANNOTSUSTAIN"]

AIRCMD_KEYWORDS = [
    "AFTBURNR", #TRUE/FALSE          HAS AFTERBURNER
	"THRAFTBN", ###[N][KG][LB]       AFTERBURNER POWER
	"THRMILIT", ###[N][KG][LB]       MILITARY POWER
	"WEIGHCLN", ###[KG][LB]          CLEAN WEIGHT
	"WEIGFUEL", ###[KG][LB]          MAX WEIGHT OF FUEL
	"WEIGLOAD", ###[KG][LB]          MAX WEIGHT OF PAYLOAD
	"FUELABRN", ###[KG][LB]          FUEL CONSUMPTION/SEC WHEN BURNER ON
	"FUELMILI", ###[KG][LB]          FUEL CONSUMPTION/SEC WHEN MIL POWER

	"LEFTGEAR", #X Y Z [M][IN]        LEFT MAIN GEAR POSITION
	"RIGHGEAR", #X Y Z [M][IN]        RIGHT MAIN GEAR POSITION
	"WHELGEAR", #X Y Z [M][IN]        WHEEL POSITION

	"CRITAOAP", ###[RAD][DEG]        CRITICAL AOA (PLUS)
	"CRITAOAM", ###[RAD][DEG]        CRITICAL AOA (MINUS

	"CRITSPED", ###[KT][KM/H][M/S][MACH]CRITICAL AIRSPEED
	"MAXSPEED", ###[KT][KM/H][M/S][MACH]MAXIMUM AIRSPEED

	"HASSPOIL", #TRUE/FALSE          HAS SPOILER
	"RETRGEAR", #TRUE/FALSE          LANDING GEAR IS RETRACTABLE
	"VARGEOMW", #TRUE/FALSE          HAS VARIABLE GEOMETRY WING

	"CLVARGEO", ###(DIMENSIONLESS)   INCREASE OF CL WHEN VGW IS EXTENDED
	"CDVARGEO", ###(DIMENSIONLESS)   INCREASE OF CD WHEN VGW IS EXTENDED
	"CLBYFLAP", ###(DIMENSIONLESS)   INCREASE OF CL WHEN FLAP FULL DOWN
	"CDBYFLAP", ###(DIMENSIONLESS)   INCREASE OF CD WHEN FLAP FULL DOWN
	"CDBYGEAR", ###(DIMENSIONLESS)   INCREASE OF CD WHEN GEAR DOWN
	"CDSPOILR", ###(DIMENSIONLESS)   INCREASE OF CD WHEN SPOILER IS DEPLOYED

	"WINGAREA", ###[M^2][IN^2]       AREA OF WING

	"MXIPTAOA", ###[RAD][DEG]           MAX INPUT AOA
	"MXIPTSSA", ###[RAD][DEG]           MAX INPUT YAW
	"MXIPTROL", ###[RAD][DEG]           MAX INPUT ROLL RATIO

	"CPITMANE", ###(DIMENSIONLESS)   PITCH MANEUVABILITY CONSTANT
	"CPITSTAB", ###(DIMENSIONLESS)   PITCH STABILITY CONSTANT
	"CYAWMANE", ###(DIMENSIONLESS)   YAW MANEUVABILITY CONSTANT
	"CYAWSTAB", ###(DIMENSIONLESS)   YAW STABILITY CONSTANT
	"CROLLMAN", ###(DIMENSIONLESS)   ROLL MANEUVABILITY CONSTANT


	"CTLLDGEA", #TRUE/FALSE          INITIAL GEAR
	"CTLBRAKE", #TRUE/FALSE          INITIAL BRAKE
	"CTLSPOIL", #0.0-1.0             INITIAL SPOILER
	"CTLABRNR", #TRUE/FALSE          INITIAL AFTERBURNER
	"CTLTHROT", #0.0-1.0             INITIAL THROTTLE
	"CTLIFLAP", #0.0-1.0             INITIAL FLAP
	"CTLINVGW", #0.0-1.0             INITIAL VGW
	"CTLATVGW", #TRUE/FALSE          INITIAL AUTO VGW

	"POSITION", #X Y Z [M][IN]
	"ATTITUDE", #H P B [DEG][RAD]
	"INITFUEL", ###[KG][LB]
	"INITLOAD", ###[KG][LB]
	"INITSPED", ###[M/S][KT][MACH]



	"REFVCRUS", ###[M/S][KM/H][KT]   CRUISING SPEED
	"REFACRUS", ###[M][FT]           CRUISING ALTITUDE
	"REFVLAND", ###[M/S][KM/H][KT]   LANDING SPEED
	"REFAOALD", ###[DEG][RAD]        AOA WHILE APPROACHING
	"REFLNRWY", ###[M][FT][KM]       RUNWAY LENGTH REQUIRED TO LAND

	"REM",

	"COCKPITP",
	"REFTHRLD",
	"REFTCRUS",

	"AUTOCALC",

	"IDENTIFY",

	"MANESPD1",
	"MANESPD2",

	"MACHNGUN",
	"SMOKEGEN",
	"HTRADIUS",
	"TRIGGER1",
	"TRIGGER2",
	"TRIGGER3",
	"TRIGGER4",

	"STRENGTH",

	"PROPELLR",

	"VAPORPO0",
	"VAPORPO1",

	"INITIGUN",
	"INITIAAM",
	"INITIAGM",

	"MANESPD3",

	"RADARCRS",

	"MACHNGN2",

	"SMOKEOIL",
	"WEAPONCH",
	"INITBOMB",

	"MONTRILS",

	"GUNPOWER",

	"CATEGORY",  # Normal,Utility or Aerobatic (+fighter, attacker)

	"VGWSPED1",  # Auto Vgw Reference Speed (Slower Speed)
	"VGWSPED2",  # Auto Vgw Reference Speed (Faster Speed)

	"GUNDIREC",  # GUN direction

	# 2001/05/06 >>
	"INITRCKT",  # Initial number of rockets
	"MAXNMGUN",  # chMaxNumGunBullet
	"MAXNMAAM",  # chMaxNumAAM               Deprecated 2010/08/04
	"MAXNMAGM",  # chMaxNumAGM               Deprecated 2010/08/04
	"MAXNMRKT",  # chMaxNumRocket            Deprecated 2010/08/04

	# 2001/06/05 >>
	"AAMSLOT_",  # chAAMSlot[chNumAAMSlot++]
	"AGMSLOT_",  # chAGMSlot[chNumAGMSlot++]
	"RKTSLOT_",  # chRocketSlot[chNumRocketSlot++]
	"BOMBSLOT",  # chBombSlot[chNumBombSlot++]
	"AAMVISIB",  # chAAMVisible;
	"AGMVISIB",  # chAGMVisible;
	"BOMVISIB",  # chBombVisible;
	"RKTVISIB",  # chRocketVisible
	"MAXNBOMB",  # chMaxNumBomb              Deprecated 2010/08/04

	# 2002/12/11 >>
	"ARRESTER",  # chArrestingHook

	# 2003/02/02 >>
	"TRSTVCTR",  # chHasThrustVector
	"TRSTDIR0",  # chThrVec0
	"TRSTDIR1",  # chThrVec1
	"PSTMPTCH",  # Post-Stall VPitch
	"PSTMYAW_",  # Post-Stall VYaw
	"PSTMROLL",  # Post-Stall VRoll

	# 2003/02/12
	"AIRCLASS",  # Aircraft class

	# 2003#02/15
	"PROPEFCY",  # Propeller efficiency
	"PROPVMIN",  # Minimum speed that T=P/v becomes valid

	# 2003/09/19
	"VRGMNOSE",  # Variable Geometry Nose : Concorde only


	# 2003/11/25
	"THRSTREV",  # Effectiveness of the Thrust Reverser


	# 2004/05/22
	"GUNSIGHT",  # Lead Gun Sight


	# 2004/06/14
	"HRDPOINT",  # Defining a hardpoint
	"LOADWEPN",  # Load weapons
	"LMTBYHDP",  # Limit weapons by hardpoint definition.
	"UNLOADWP",  # Unload All Weapons (Missiles, Bombs, Rockets.  Excluding Guns, Smokes, and Flare)

	# 2005/01/03
	"INSTPANL",  # Draw an instrument panel instead of a hud. (av[1] for inst panel definition file.)

	# 2005/01/05
	"MACHNGN3",
	"MACHNGN4",
	"MACHNGN5",
	"MACHNGN6",
	"MACHNGN7",
	"MACHNGN8",

	# 2005/01/11
	"BOMINBAY",
	"BMBAYRCS",

	# 2005/01/23
	"INITAAMM",  # Mid-Range AAM
	"MAXNAAMM",  # Max # Mid-Range AAM
	"INITB250",  # 250lb Bomb
	"MAXNB250",  # Max # 250lb Bomb

	# 2005/03/08
	"GUNINTVL",  # Gun Interval

	# 2005/06/26
	"NMTURRET",  # Number of turret
	"TURRETPO",  #  0 0m -0.8m 2.7m 0deg 0deg 0deg      # Number x y z h p b
	"TURRETPT",  #  0 -40deg 0deg 0deg                  # Number MinPitch MaxPitch NeutralPitch
	"TURRETHD",  #  0 -120deg 120deg 0deg               # Number MinHdg MaxHdg NeutralHdg
	"TURRETAM",  #  0 0                                 # Ammo(zero -> staGunBullet will be used)
	"TURRETIV",  #  0 0.5sec                            # Number ShootingInterval
	"TURRETNM",  #  0 GUN                               # DNM Node Name
	"TURRETAR",  #  0 FALSE                             # TRUE -> Anti Air Capable
	"TURRETGD",  #  0 TRUE                              # TRUE -> Anti Ground Capable
	"TURRETCT",  #  "PILOT" or "GUNNER"
	"TURRETRG",  #  Range
	# 2005/09/28
	"TURRETNH",  # DNM Node Name (Heading Rotation)
	"TURRETNP",  # DNM Node Name (Pitch Rotation)

	# 2006/04/25
	"SETCNTRL",  # Set Control eg. ILS TRIM:0.3 etc.

	# 2006/07/19
	"EXCAMERA",  # Extra Camera

	# 2006/08/05
	"NMACHNGN",  # Number of machine guns.

	# 2007/04/06
	"SMOKECOL",  # Smoke Color #dmy# R G B

	# 2007/09/16
	"SUBSTNAM",  # Substitute airplane (In case the airplane was not installed)

	# 2010/06/26
	"ISPNLPOS",  # Instrument Panel Position
	"ISPNLSCL",  # Instrument Panel Scaling

	# 2010/06/29
	"ISPNLHUD",  # Use both inst panel and HUD
	"COCKPITA",  # Neutral Head Direction

	# 2010/06/30
	"SCRNCNTR",  # Screen center (Relative.  (-1.0,-1.0)-(1.0,1.0)
	"ISPNLATT",  # Instrument Panel Orientation
	"MAXNMFLR",  # Maximum number of flare

	# 2010/07/01
	"FLAPPOSI",  # Flap position
	"FLAREPOS",  # Flare Dispenser Position and Direction

	# 2010/12/11
	"INITAAAM",  # Initialize AIM9X
	"INITHDBM",  # Initialize High-Drag bomb
	"ULOADAAM",  # Unload all AAMs
	"ULOADAGM",  # Unload all AGMs
	"ULOADBOM",  # Unload all Bombs
	"ULOADFLR",  # Unload all Flare
	"ULOADGUN",  # Unload all Gun
	"ULOADRKT",  # Unload all Rocket

	# 2011/12/25
	"LOOKOFST",  # Look-at Offset

	# 2012/02/02
	"WPNSHAPE",  # Weapon-shape override

	# 2012/02/21
	"GEARHORN",  # Landing-gear warning horn
	"STALHORN",  # Stall-warning horn

	# 2013/04/14
	"CKPITIST",  # To Make inst panel available in only one of EXCAMERAs, it can be hidden in the default cockpit view.
	"CKPITHUD",  # To Make HUD available in only one of EXCAMERAs, it can be hidden in the default cockpit view.

	# 2013/04/25
	"MALFUNCT",  # Malfunction
	"REPAIRAL",  # Repair all

	# 2013/04/25
	"REPAIRFN",  # Repair functionality

	# 2013/06/02
	"NOLDGFLR",  # No landing flare

	# 2014/06/05
	"NREALPRP",  # Number of (real) propeller engines
	"REALPROP",  # Support for realistic propeller engine

	# 2014/06/13
	"TIREFRIC",  # Tire friction coefficient

	# 2014/06/24
	"PSTMSPD1",   # Maximum speed that the direct attitude control is fully effective.
	"PSTMSPD2",   # Speed at which the direct attitude control becomes ineffective.
	"PSTMPWR1",   # Minimum required power setting for direct attitude control
	"PSTMPWR2",   # Power setting at which the direct attitude control is fully effective

	# 2014/07/11
	"MAXCDAOA",
	"FLATCLR1",
	"FLATCLR2",
	"CLDECAY1",
	"CLDECAY2",

	# 2014/10/17
	"AIRSTATE",  # I'm shocked that I didn't have it yet.

	# 2018/10/07
	"INITZOOM",  # Initial zoom factor

	None
]
