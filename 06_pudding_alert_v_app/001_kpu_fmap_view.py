## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import image, lcd, sensor
import KPU as kpu
from fpioa_manager import fm

def m5stickv_init():
    lcd.init()
    lcd.rotation(2)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA) #QVGA=320x240
    sensor.set_windowing((224, 224))
    sensor.run(1)
    fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
    but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!
    fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
    but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

m5stickv_init()

but_a_pressed = 0
but_b_pressed = 0

dummyImage = image.Image()
dummyImage = dummyImage.resize(32, 24)
kpu_dat = dummyImage.to_grayscale(1)

task = kpu.load("mbnet751.kmodel")

set=kpu.set_layers(task,29)

while(True):
    img = sensor.snapshot()
    fmap = kpu.forward(task, img)
    plist=fmap[:]
    for row in range(32):
        for col in range(24):
            kpu_dat[24*row+col] = int(plist[row*24+col]*100)
    img2=img.resize(100,100)
    img3=kpu_dat.resize(100,100)
    lcd.display(img2,oft=(10,16))
    lcd.display(img3,oft=(120,16))
