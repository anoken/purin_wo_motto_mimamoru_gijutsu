## Copyright (c) 2019 aNoken
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu


import lcd
from Maix import I2S, GPIO
from fpioa_manager import fm
from board import board_info

lcd.init()
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0

while(True):
    if but_a.value() == 0 and but_a_pressed == 0:
        print("A_push")
        but_a_pressed=1
    if but_a.value() == 1 and but_a_pressed == 1:
        print("A_release")
        but_a_pressed=0

    if but_b.value() == 0 and but_b_pressed == 0:
        print("B_push")
        but_b_pressed=1
    if but_b.value() == 1 and but_b_pressed == 1:
        print("B_release")
        but_b_pressed=0
