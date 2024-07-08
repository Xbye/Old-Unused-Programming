import os
import time
from datetime import datetime
import sys

PATH_STEAMCMD = "/home/xbye/Steam/steamcmd.sh"
PATH_L4D2 = "/home/xbye/Steam/steamapps/common/l4d2"
PATH_CACHE_ID = "/home/xbye/Steam/steamapps/common/l4d2/left4dead2/SRCDS_Version.txt"

CMD_STOPSERVER = "/bin/bash /home/xbye/Steam/steamapps/common/l4d2/left4dead2/stopl4d2"
CMD_STARTSERVER = "/bin/bash /home/xbye/Steam/steamapps/common/l4d2/left4dead2/startl4d2"
APP_ID = "222860"

TIMER_INVALIDATE = 21600
DEBUG_MODE = True

# If DEBUG_MODE is True, then every function will print when entered.
def debugLog(msg):
    if(DEBUG_MODE):
        humanly_readable = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{humanly_readable}] {msg}")

def getInstalledSRCDS():
    debugLog(sys._getframe().f_code.co_name)

    ensureInstalledSRCDS_cache()

    return open(PATH_CACHE_ID, "r").read()

# Queries SteamCMD for the current version of SRCDS L4D2 app (222860)
def updateInstalledSRCDS_cache():
    debugLog(sys._getframe().f_code.co_name)

    command = [
        f"{PATH_STEAMCMD} << END_TEXT | grep BuildID | awk '{{print $NF}}'",
        f"force_install_dir {PATH_L4D2}",
        f"login anonymous",
        f"app_status {APP_ID}",
        f"quit",
        f"END_TEXT"
    ]

    buildID =  os.popen(os.linesep.join(command)).read().strip()

    #Write the version to a file, to check later to minimize how often we run SteamCMD
    file_version = open(PATH_CACHE_ID, "w")
    file_version.write(buildID)
    file_version.close()

# If the version file is too old, then we need to update it (validation)
def ensureInstalledSRCDS_cache():
    debugLog(sys._getframe().f_code.co_name)

    if os.path.isfile(PATH_CACHE_ID) and time.time() < os.path.getmtime(PATH_CACHE_ID) + TIMER_INVALIDATE:
        return

    updateInstalledSRCDS_cache()


def getValveSRCDS():
    debugLog(sys._getframe().f_code.co_name)

    command = [
        f"{PATH_STEAMCMD} << END_TEXT | grep buildid | awk '{{print $NF}}' | head -n 1 | tr -d '\"' ",
        f"force_install_dir {PATH_L4D2}",
        f"login anonymous",
        f"app_info_print {APP_ID}",
        f"quit",
        f"END_TEXT"
    ]

    return os.popen(os.linesep.join(command)).read().strip()

def shutdownServers():
    debugLog(sys._getframe().f_code.co_name)
    os.system(CMD_STOPSERVER)


def startServers():
    debugLog(sys._getframe().f_code.co_name)
    os.system(CMD_STARTSERVER)


def updateServers():
    debugLog(sys._getframe().f_code.co_name)
    print("Updating Server")

    shutdownServers()

    command = [
        f"{PATH_STEAMCMD} << END_TEXT",
        f"force_install_dir {PATH_L4D2}",
        f"login anonymous",
        f"app_update {APP_ID}",
        f"quit",
        f"END_TEXT"
    ]

    os.system(os.linesep.join(command))
    updateInstalledSRCDS_cache()
    startServers()


versionInstalled = getInstalledSRCDS()
versionValve = getValveSRCDS()

if not versionInstalled.isdigit() or not versionValve.isdigit():
    print(f"error {versionInstalled} {versionValve}")
    quit()

if(versionInstalled < versionValve):
    updateServers()
else:
    print("No Update")