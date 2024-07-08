import pathlib
import subprocess

HOME = pathlib.Path.home()
SRCDS_L4D2 = pathlib.Path.joinpath(HOME, "Steam/steamapps/common/l4d2/srcds_run")

SVR_COUNT = 8
SVR_PORT = 27020
SVR_GROUP_COUNT = 4
SVR_NAME = "Public_Community_Servers"

if(not SRCDS_L4D2.exists()):
    print("srcds_linux for l4d2 could not be found")
else:
    print("srcds_linux found")

subprocess.run(f'screen -dmS l4d2.py_27015 {SRCDS_L4D2} -port 27015 +hostname "{SVR_NAME}_#XED" +servercfgfile servervip.cfg', shell=True)
subprocess.run(f'screen -dmS l4d2.py_27016 {SRCDS_L4D2} -port 27016 +hostname "{SVR_NAME}_#LIZ" +servercfgfile servervip.cfg', shell=True)
subprocess.run(f'screen -dmS l4d2.py_27017 {SRCDS_L4D2} -port 27017 +hostname "{SVR_NAME}_#ZAL" +servercfgfile servervip.cfg', shell=True)
for x in range(SVR_PORT, SVR_PORT + SVR_COUNT):
    if x < SVR_PORT + SVR_GROUP_COUNT:
        subprocess.run(f'screen -dmS l4d2.py_{x} {SRCDS_L4D2} -port {x} +hostname "{SVR_NAME}_#{x - SVR_PORT + 1}" +servercfgfile servergroup.cfg', shell=True)
    else:
        subprocess.run(f'screen -dmS l4d2.py_{x} {SRCDS_L4D2} -port {x} +hostname "{SVR_NAME}_#{x - SVR_PORT + 1}" +servercfgfile serverpub.cfg', shell=True)
