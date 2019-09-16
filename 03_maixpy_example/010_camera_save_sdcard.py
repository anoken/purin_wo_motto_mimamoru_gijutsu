## Copyright (c) 2019 aNoken
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor, image,lcd,os
from fpioa_manager import fm
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)
is_button_a = 0
is_button_b = 0

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

path = "save/"
ext=".jpg"
cnt=0
img_read = image.Image()

#os.mkdir("save")
print(os.listdir())

while True:
    if is_button_b == 1:
        lcd.display(img_read)

    else :
        img=sensor.snapshot()
        lcd.display(img)

    if but_a.value() == 0 and is_button_a == 0:
        print("save image")
        cnt+=1
        fname=path+str(cnt)+ext
        print(fname)
        img.save(fname, quality=95)
        is_button_a=1

    if but_a.value() == 1 and is_button_a == 1:
        is_button_a=0

    if but_b.value() == 0 and is_button_b == 0:
        fname=path+str(cnt)+ext
        print(fname)
        img_read = image.Image(fname)
        is_button_b=1

    if but_b.value() == 1 and is_button_b == 1:
        is_button_b=0
