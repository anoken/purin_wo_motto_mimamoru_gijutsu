## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


import os
devices = os.listdir("/")

if "flash" in devices:
    os.chdir("/flash")
    print("flash")
    print(os.listdir())
if "sd" in devices:
    os.chdir("/sd")
    print("sd")
    print(os.listdir())
