## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


import sensor
import image
import lcd
from fpioa_manager import *
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

isButtonPressedA = 0
isButtonPressedB = 0

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

path = "/sd/image.jpg"
img_read = image.Image()

while True:
    if isButtonPressedB == 1:
        lcd.display(img_read)

    else :
        img=sensor.snapshot()
        lcd.display(img)

    if but_a.value() == 0 and isButtonPressedA == 0:
        print("save image")
        img.save(path, quality=95)
        isButtonPressedA=1

    if but_a.value() == 1 and isButtonPressedA == 1:
        isButtonPressedA=0

    if but_b.value() == 0 and isButtonPressedB == 0:
        img_read = image.Image(path)
        isButtonPressedB=1

    if but_b.value() == 1 and isButtonPressedB == 1:
        isButtonPressedB=0
