## Copyright (c) 2019 aNoå§ ÉvÉäÉìÇÇ‡Ç¡Ç∆å©éÁÇÈãZèp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor,image,lcd
import KPU as kpu
from fpioa_manager import *
from Maix import GPIO
from board import board_info
from fpioa_manager import fm
fm.register(board_info.LED_R, fm.fpioa.GPIO4)
led_r = GPIO(GPIO.GPIO4, GPIO.OUT)
led_r.value(1)

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
task = kpu.load("facedetect.kmodel")

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
img_lcd=image.Image()
while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    face_detec=False
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect())
            face_detec=True
    if face_detec:
        led_r.value(0)
    else:
        led_r.value(1)

    a = lcd.display(img)
a = kpu.deinit(task)
