## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor, image, lcd, time
from fpioa_manager import fm
from Maix import I2S, GPIO

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
origin = (0,0,0, 0,1,0, 0,0,0)
edge = (-1,-1,-1,-1,8,-1,-1,-1,-1)
sharp = (-1,-1,-1,-1,9,-1,-1,-1,-1)
relievo = (2,0,0,0,-1,0,0,0,-1)
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
but_a_pressed = 0
but_b_pressed = 0
cnt=0
while True:
    if but_a.value() == 0 and but_a_pressed == 0:
        cnt=cnt+1
        print("A_push")
        but_a_pressed=1
    if but_a.value() == 1 and but_a_pressed == 1:
        print("A_release")
        but_a_pressed=0

    img=sensor.snapshot()
    if cnt==1:
        img.conv3(edge)
        img.draw_string(10,60, "edge",color=(255,0,0))
    elif cnt==2:
        img.conv3(sharp)
        img.draw_string(10,60, "sharp",color=(255,0,0))
    elif cnt==3:
        img.conv3(relievo)
        img.draw_string(10,60, "relievo",color=(255,0,0))
    else :
        cnt=0
    lcd.display(img)
