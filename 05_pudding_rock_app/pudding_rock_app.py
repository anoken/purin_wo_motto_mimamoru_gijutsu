## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor,image,lcd,time
from fpioa_manager import fm, board_info
from Maix import GPIO

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)
sensor.skip_frames(30)

fm.register(34, fm.fpioa.GPIOHS0, force=True)
fm.register(35, fm.fpioa.GPIOHS1, force=True)

pinout34 = GPIO(GPIO.GPIOHS0, GPIO.OUT)
pinout34.value(0)
pinout35 = GPIO(GPIO.GPIOHS1, GPIO.OUT)
pinout35.value(0)

string_code="https://line.naver.jp/ti/p/@user_name"

while True:
    img = sensor.snapshot()
    res = img.find_qrcodes()
    if len(res) > 0:
        print(res[0].payload())
        if res[0].payload()==string_code:
            img.draw_rectangle(1,46,222,132,color=31,thickness=3)
            img.draw_string(1,46, res[0].payload(), color=(0,128,0), scale=1)
            pinout35.value(1)
            pinout34.value(1)
        else :
            pinout35.value(0)
            pinout34.value(0)
    lcd.display(img)
