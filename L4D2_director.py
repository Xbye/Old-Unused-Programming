# Script made by Xbye and Luckylock
# Python script to help manage different things with L4D2 SRCDS

import os
import sys
import time
import argparse

GAME_ID = "550"
SRCDS_ID = "222860"

DEFAULT_TICKRATE = "30"
DEFAULT_COUNT = "8"
DEFAULT_SERVERNAME = "/r/L4D2"

PATH_STEAMCMD_DEFAULT = "./"
PATH_INSTALL_DEFAULT = "./steampapps/common/L4D2SVR/"
PATH_SRCDS_ID_DEFAULT = f"{PATH_INSTALL_DEFAULT}_SRCDS_BuildID.txt"
PATH_GAME_ID_DEFAULT = f"{PATH_INSTALL_DEFAULT}_Game_BuildID.txt"

# 21600 = 6 hours // 3600 = 1 hours
TIMER_INVALIDATE = 3600 
TIMER_HOLD_SRCDS_UPDATE = 21600

# Should we query SteamCMD servers a 3rd time after a successful update.
FORCE_APPSTATUS_ON_UPDATE = False

DEBUG_MODE = 4

def debugFormat(msg, level):
    timestamp = time.strftime("%m-%d-%Y @ %I:%M", time.localtime())
    print(f"[{timestamp}] D:{level} - {msg}")

def main():
    script_start = time.time()

    if(DEBUG_MODE > 0):
        debugFormat("The director is running...", 1)

    parseinput = argparse.ArgumentParser()
    exclusive = parseinput.add_mutually_exclusive_group()

    exclusive.add_argument("--update", action="store_true", default=False,
                            help="Force update SRCDS. [--update -dir FOLDER]")
    exclusive.add_argument("--start", action="store_true", default=False,
                            help="Runs the script to start servers. [--start -c ## -t ##]")
    exclusive.add_argument("--stop", action= "store_true", default = False,
                            help="Runs the script to stop servers.")
    exclusive.add_argument("--workshop", action= "store_true", default = False,
                            help="Pulls a map from Steam workshop. [--workshop -w #######]")
    exclusive.add_argument("--pull", action= "store_true", default = False,
                            help="Prints stored versions, and Steam server's versions")
    exclusive.add_argument("--install", action= "store_true", default = False,
                            help="Installs SRCDS and SourceMod.")
    exclusive.add_argument("--sourcemod", action= "store_true", default = False,
                            help="Attempts to pull gamedata. (Not working right now)")
    exclusive.add_argument('--version', action='version', version='L4D2_Director v0.1')

    parseinput.add_argument("-dir", "-d", nargs = 1, type=str, default=PATH_INSTALL_DEFAULT,
                            help="Selects directory, used for install/update.")
    parseinput.add_argument("-count", "-c", nargs = 1, type=str, default=DEFAULT_COUNT,
                            help="Amount of servers, used for start.")
    parseinput.add_argument("-tick", "-t", nargs = 1, type=str, default=DEFAULT_TICKRATE,
                            help="Server tickrate, used for start.")
    parseinput.add_argument("-force", "-f", action="store_true", default = False,
                            help="Bypass any prompts, using defaults.")

    args = parseinput.parse_args()



    if(args.update):
        debugFormat(f"Beginning SRCDS update process.", 1)
        
        if(args.dir == PATH_INSTALL_DEFAULT and not args.force):
            print("You can use -f to skip these prompts and use defaults.")
            userinput = str(input(f"Provide L4D2 directory. (Leave blank to use default [{PATH_INSTALL_DEFAULT}]):\n> "))

            if(userinput != ""):
                args.dir = userinput

        debugFormat(f"Updating SRCDS @ {args.dir}", 1)

    elif(args.start):
        debugFormat(f"Starting up servers.", 1)
    elif(args.stop):
        debugFormat(f"Stopping servers.", 1)
    elif(args.workshop):
        debugFormat(f"Workshop searching.", 1)
    elif(args.pull):
        debugFormat(f"Comparing stored versions to SteamCMD.", 1)
    elif(args.install):
        debugFormat(f"Installing L4D2 SRCDS.", 1)
    elif(args.sourcemod):
        debugFormat(f"Sourcemod doesn't work right now.", 1)
    else:
        debugFormat(f"Checking if there are any updates.", 1)

    if(DEBUG_MODE > 3):
        debugFormat(f"--update: {args.update}", 3)
        debugFormat(f"--start: {args.start}", 3)
        debugFormat(f"--stop: {args.stop}", 3)
        debugFormat(f"--workshop: {args.workshop}", 3)
        debugFormat(f"--pull: {args.pull}", 3)
        debugFormat(f"--install: {args.install}", 3)
        debugFormat(f"--sourcemod: {args.sourcemod}", 3)

    if(DEBUG_MODE > 3):
        debugFormat(f"--dir: {args.dir}", 3)
        debugFormat(f"--count: {args.count}", 3)
        debugFormat(f"--tick: {args.tick}", 3)
        debugFormat(f"--force: {args.force}", 3)

    
    
    print("Runtime:", time.strftime("%H:%M:%S", time.gmtime(time.time() - script_start)))

if __name__=="__main__": 
    main() 