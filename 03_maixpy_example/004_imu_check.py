## Copyright (c) 2019 aNoŒ¤ ƒvƒŠƒ“‚ğ‚à‚Á‚ÆŒ©ç‚é‹Zp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from machine import I2C
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print(devices)
