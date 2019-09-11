## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import image, lcd, sensor
import KPU as kpu
from fpioa_manager import fm
from Maix import GPIO

def m5stickv_init():
    lcd.init()
    lcd.rotation(2)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA) #QVGA=320x240
    sensor.set_windowing((224, 224))
    sensor.run(1)
    fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
    but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
    fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
    but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

m5stickv_init()
task = kpu.load("mbnet751.kmodel")
set=kpu.set_layers(task,29)

but_a_pressed = 0
but_b_pressed = 0

s_data = []
for i in range(768):
    s_data.append(0)
w_data=0.9


while(True):
    img = sensor.snapshot()
    fmap = kpu.forward(task, img)
    plist=fmap[:]

    dist = 0
    if but_a.value() == 0 and but_a_pressed == 0:
        firstmap = kpu.forward(task,img)
        firstdata = firstmap[:]
        for i in range(768):
            s_data[i] =firstdata[i]
        but_a_pressed=1

    if but_a.value() == 1 and but_a_pressed == 1:
        but_a_pressed=0

    for i in range(768):
        dist = dist + (plist[i]-s_data[i])**2

    if dist < 100:
        for i in range(768):
            s_data[i] =w_data*s_data[i]+ (1.0-w_data)*plist[i]

    if dist < 200:
        img.draw_rectangle(1,46,222,132,color = (0, 0, 255),thickness=5)
    else:
        img.draw_rectangle(1,46,222,132,color = (255, 0, 0),thickness=5)

    img.draw_string(2,47,  "%.2f "%(dist))
    lcd.display(img)
