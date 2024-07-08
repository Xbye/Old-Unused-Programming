import time
import argparse
import pathlib
import subprocess

# Print Levels:
DEBUG = 1

# SteamCMD must be in the same folder as this script
PATH_STEAMCMD = pathlib.Path.cwd().joinpath("steamcmd.sh")
PATH_FORCE_INSTALL_DIR = pathlib.Path.home().joinpath("steamapps/common/L4D2SVR")
SERVER_NAME = "/r/L4D2"
TICKRATE = 30
AMT_SERVER = 3
PORT_START = 27045 # Starting port

# Needed for Worshop Downloading
LOGIN_STEAMCMD = ""
PASS_STEAMCMD = ""

# Refresh: How often we should update SRCDS.txt and GAME.txt
# Hold_update: Should we hold back SRCDS updates if no game update found?
TIMER_REFRESH = 3600
TIMER_HOLD_UPDATE = 21600

# Should we query SteamCMD servers a third time after a successful update.
FORCE_APPSTATUS_ON_UPDATE = False

GAME_ID = "550"
SRCDS_ID = "222860"

def debugFormat(msg, level):
    timestamp = time.strftime("%m-%d-%Y @ %I:%M", time.localtime())
    print(f"[{timestamp}] D:{level} - {msg}")

def shutdownServers():
    if(DEBUG > 0):
        debugFormat(f"Shutting down L4D2 screens.", 1)

    subprocess.run("screen -ls | grep l4d2.py | awk \'{print $1}\' | xargs -I{} screen -XS {} stuff 'sm_cvar sv_cheats 1^M;quit^M' ", shell=True)

def startupServers(path):
    if(DEBUG > 0):
        debugFormat(f"Starting up L4D2 screens", 1)

    for x in range(PORT_START, PORT_START + AMT_SERVER):
        subprocess.run(f"screen -dmS l4d2.py_{x} '{path}' -port {x} +{SERVER_NAME}", shell=True)

def updateServers(path):

    if(DEBUG > 0):
        debugFormat(f"Attempting to update {path}", 1)

    command_execute = [
        f"{PATH_STEAMCMD} << END_TEXT",
        f"force_install_dir \"{path}\"",
        f"login anonymous",
        f"app_update {SRCDS_ID}",
        f"quit",
        f"END_TEXT"
    ]

    #os.system(os.linesep.join(command_execute))

def checkVersions(path):
    print("WIP")
    

def prompt(default,msg):
    print(msg)
    userinput = input(f"[DEFAULT: {default}]:")

    if(len(userinput) == 0 or userinput.isspace()):
        return default
    else:
        return userinput

def main():
    if(DEBUG > 0):
        debugFormat("The director is running...", 1)

    cmdline = argparse.ArgumentParser()
    exclusive = cmdline.add_mutually_exclusive_group()

    exclusive.add_argument("--update", action="store_true", default=False,
                            help="Force update SRCDS. [--update DIRECTORY]")
    exclusive.add_argument("--start", action="store_true", default=False,
                            help="Runs the script to start servers. [--start AMT TICK]")
    exclusive.add_argument("--stop", action= "store_true", default = False,
                            help="Runs the script to stop servers.")
    exclusive.add_argument("--workshop", action= "store_true", default = False,
                            help="Pulls a map from Steam workshop. [--workshop WORKSHOPID WORKSHOPID... WORKSHOPID]")
    exclusive.add_argument("--pull", action= "store_true", default = False,
                            help="Prints stored versions, and Steam server's versions")
    exclusive.add_argument("--install", action= "store_true", default = False,
                            help="Installs SRCDS and SourceMod.")
    exclusive.add_argument("--sourcemod", action= "store_true", default = False,
                            help="Attempts to pull gamedata. (Not working right now)")
    exclusive.add_argument('--version', action='version', version='L4D2_Director v0.1')    

    cmdline.add_argument("dir", nargs="*", type=str)
    cmdline.add_argument("-force", "-f", action="store_true", default = False,
                        help="Bypass any prompts, using program defaults. Ignores options.")

    args = cmdline.parse_args()

    if(args.update):

        if(len(args.OPTIONS) > 0):
            force_install_dir = args.OPTIONS[0]
        elif(not args.force):
            force_install_dir = pathlib.Path(prompt(PATH_FORCE_INSTALL_DIR,"Provide a directory, or use the default?"))
        else:
            force_install_dir = PATH_FORCE_INSTALL_DIR
        
        if(not pathlib.Path(force_install_dir).joinpath('srcds_run').exists()):
            if(DEBUG > 0):
                debugFormat(f"ERROR: \"{str(force_install_dir.joinpath('srcds_run'))}\" does not exist on machine. Aborting.", 1)
            quit()
        else:
            shutdownServers()
            updateServers(str(force_install_dir))
            startupServers(str(force_install_dir))

    elif(args.start):

        if(len(args.OPTIONS) > 0):
            force_install_dir = args.OPTIONS[0]
        elif(not args.force):
            force_install_dir = pathlib.Path(prompt(PATH_FORCE_INSTALL_DIR,"Provide a directory, or use the default?"))
        else:
            force_install_dir = PATH_FORCE_INSTALL_DIR
        
        if(not pathlib.Path(force_install_dir).joinpath('srcds_run').exists()):
            if(DEBUG > 0):
                debugFormat(f"ERROR: \"{str(force_install_dir.joinpath('srcds_run'))}\" does not exist on machine. Aborting.", 1)
            quit()
        else: 
            startupServers(str(force_install_dir.joinpath('srcds_run')))

    elif(args.stop):

        shutdownServers()

    elif(args.workshop):
        print("WIP3")
    elif(args.install):
        print("WIP4")
    elif(args.sourcemod):
        print("WIP5")
    else:

        if(len(args.OPTIONS) > 0):
            force_install_dir = args.OPTIONS[0]
        elif(not args.force):
            force_install_dir = pathlib.Path(prompt(PATH_FORCE_INSTALL_DIR,"Provide a directory, or use the default?"))
        else:
            force_install_dir = PATH_FORCE_INSTALL_DIR

        if(not pathlib.Path(force_install_dir).joinpath('srcds_run').exists()):
            if(DEBUG > 0):
                debugFormat(f"ERROR: \"{str(force_install_dir.joinpath('srcds_run'))}\" does not exist on machine. Aborting.", 1)
            quit()
        else:
            print("WIP6")

    if(DEBUG > 3):
        debugFormat(f"OPTIONS: {args.OPTIONS}", 3)

if __name__=="__main__":
    main()