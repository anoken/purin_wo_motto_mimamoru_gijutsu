## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import lcd  #for test
from machine import I2C
AXP192_ADDR=0x34
cmd=0xF0		#range(0x70-0xF0)

i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
i2c.writeto_mem(AXP192_ADDR, cmd)
