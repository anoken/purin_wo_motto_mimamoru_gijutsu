## Copyright (c) 2019 aNoŒ¤ ƒvƒŠƒ“‚ğ‚à‚Á‚ÆŒ©ç‚é‹Zp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor,image,lcd
lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
while True:
    img=sensor.snapshot()
    lcd.display(img)
