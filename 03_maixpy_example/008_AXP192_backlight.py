## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu
import lcd  #for test
from machine import I2C
AXP192_ADDR=0x34
Backlight_ADDR=0x91
level=50
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
val = (level+7) << 4
i2c.writeto_mem(AXP192_ADDR, Backlight_ADDR,int(val))

