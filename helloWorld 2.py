# Script made by Luckylock & Xbye
# Auto-updates a Steam application, noteably, L4D2.
# Python3

import os
import sys
import time
from datetime import datetime

PATH_STEAMCMD = "/home/xbye/steamcmd.sh"
PATH_L4D2 =  "/home/xbye"
PATH_CACHE_ID = "/home/xbye/steamapps/common/L4D2SVR/left4dead2/SRCDS_Version.txt"

# Only checking SRCDS L4D2, not 550 L4D2
APP_ID = "222860"

CMD_STOPSERVER = "/bin/bash /home/xbye/scripts_steamcmd/stopl4d2.sh"
CMD_STARTSEREVER = "/bin/bash /home/xbye/scripts_steamcmd/startl4d2.sh"

# How long until we force re-write to SRCDS_Version.txt
TIMER_INVALIDATE = 21600 #6 hours

# Whether we should run cmdSteamCMD_SRCDS_app_status() 
# AGAIN to save into SRCDS_Version.txt or use the stored
# variable we grabbed from cmdSteamCMD_SRCDS_app_info_print()
# during the update.
FORCE_APP_STATUS_ON_UPDATE = False

# Values from 0 - 3 : Higher values = More print logs : 0 meaning no prints
# 0 : No prints
# 1 : Script progress prints
# 2 : Script runtime and other things
# 3 : Function name prints and in-function buildID prints
DEBUG_MODE = 2

def printDebugMSG(msg, level):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [D{level}] {msg}")

def getInstalled_SRCDS():
    
    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(sys._getframe().f_code.co_name, 3)
    
    if readInstalled_SRCDS():
        cmdSteamCMD_SRCDS_app_status()
    
    return open(PATH_CACHE_ID, "r").read()


def readInstalled_SRCDS():

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(sys._getframe().f_code.co_name, 3)

    # Checks how old SRCDS_VERSION.TXT is.
    if not os.path.isfile(PATH_CACHE_ID):
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("SRCDS_version.txt does not exist, creating one.", 1)
        return True
    elif time.time() > os.path.getmtime(PATH_CACHE_ID) + TIMER_INVALIDATE:
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("SRCDS_version.txt is too old, must query SteamCMD for current version.", 1)
        return True
    else:
        return False

def cmdSteamCMD_SRCDS_app_status():

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(sys._getframe().f_code.co_name, 3)

    command_execute = [
        f"{PATH_STEAMCMD} << END_TEXT | grep BuildID | awk '{{print $NF}}'",
        f"force_install_dir \"{PATH_L4D2}\"",
        f"login anonymous",
        f"app_status {APP_ID}",
        f"quit",
        f"END_TEXT"   
    ]

    Build_ID = os.popen(os.linesep.join(command_execute)).read().strip()

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(f"app_status : [{Build_ID}]", 3)

    # Validate we received a number from Valve.
    if(Build_ID.isdigit()):
        SRCDS_versionTXT = open(PATH_CACHE_ID, "w")
        SRCDS_versionTXT.write(Build_ID)
        SRCDS_versionTXT.close()
    else:
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("Exiting script: app_status did not receive what we wanted from Valve.", 1)
        sys.exit()

def cmdSteamCMD_SRCDS_app_info_print():

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(sys._getframe().f_code.co_name, 3)
    
    command_execute = [
        f"{PATH_STEAMCMD} << END_TEXT | grep buildid | awk '{{print $NF}}' | head -n 1 | tr -d '\"' ",
        f"force_install_dir \"{PATH_L4D2}\"",
        f"login anonymous",
        f"app_info_print {APP_ID}",
        f"quit",
        f"END_TEXT"
    ]

    Build_ID = os.popen(os.linesep.join(command_execute)).read().strip()

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(f"app_info_print : [{Build_ID}]", 3)

    # Validate we received a number from Valve.
    if(Build_ID.isdigit()):
        return Build_ID
    else:
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("Exiting script: app_info_print did not receive what we wanted from Valve.", 1)
        sys.exit() 

def updateServers():

    if(DEBUG_MODE > 2): # Level 3
        printDebugMSG(sys._getframe().f_code.co_name, 3)

    if(DEBUG_MODE > 0): # Level 1
        printDebugMSG("New update found! Updating servers...", 1)

    if(os.path.isfile(CMD_STOPSERVER)):
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("Shutting down servers.", 1)
        
        os.system(CMD_STOPSERVER)
    
    command_execute = [
        f"{PATH_STEAMCMD} << END_TEXT",
        f"force_install_dir \"{PATH_L4D2}\"",
        f"login anonymous",
        f"app_update {APP_ID}",
        f"quit",
        f"END_TEXT"
    ]

    os.system(os.linesep.join(command_execute))

    if(os.path.isfile(CMD_STARTSEREVER)):
        if(DEBUG_MODE > 0): # Level 1
            printDebugMSG("Starting up servers.", 1)
        
        os.system(CMD_STARTSEREVER)

########## Code Starts Below ##########

if(DEBUG_MODE > 1): # Level 2
    script_runtime = time.time()

version_installedSRCDS = getInstalled_SRCDS()
version_ValveSRCDS = cmdSteamCMD_SRCDS_app_info_print()

if(DEBUG_MODE > 1): # Level 2
    printDebugMSG(f"Installed: {version_installedSRCDS} || Valve: {version_ValveSRCDS}", 2)

if(version_installedSRCDS < version_ValveSRCDS):
    updateServers()

    if(FORCE_APP_STATUS_ON_UPDATE):
        newUpdateVersion = getInstalled_SRCDS()
    else:
        newUpdateVersion = version_ValveSRCDS

    if(DEBUG_MODE > 1): # Level 2
        printDebugMSG(f"Writing {newUpdateVersion} to SRCDS_version.txt.", 2)
    
    SRCDS_versionTXT = open(PATH_CACHE_ID, "w")
    SRCDS_versionTXT.write(newUpdateVersion)
    SRCDS_versionTXT.close()
        
elif(DEBUG_MODE > 0): # Level 1
    printDebugMSG("No update was found.", 1)

if(DEBUG_MODE > 1): # Level 2
    print("Script runtime:", time.strftime("%H:%M:%S", time.gmtime(time.time() - script_runtime)))
    #Seems to only work on newer Python versions...
    #print(f"Script runtime: {time.strftime("%H:%M:%S", time.gmtime(time.time() - script_runtime))}")