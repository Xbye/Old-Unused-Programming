# import pathlib
# import argparse

# SRCDS_ID_TXT = "SRCDS_BUILDID.txt"

# test_cwd_path = pathlib.Path.cwd()
# # e:\CEDA\CEDA JUNK
# test_L4D2_director = pathlib.Path(pathlib.PurePath(test_cwd_path).joinpath("L4D2_Director.py")).exists()

# print(test_cwd_path)

# print(test_cwd_path.exists())
# print(test_L4D2_director)

# test_write_cwd_dir = test_cwd_path.joinpath(SRCDS_ID_TXT)
# #test_write_cwd_dir.mkdir(parents=True, exist_ok=True)
# print(test_write_cwd_dir)
# with test_write_cwd_dir.open("w", encoding="utf-8") as f:
#     f.write("19900")

userinput = input("> ")

print(len(userinput))
print(len(userinput) == 0 or userinput.isspace())