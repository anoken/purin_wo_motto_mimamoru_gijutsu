## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu



import time,math
from machine import Timer,PWM
from fpioa_manager import fm
from board import board_info

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
PWM_ch = PWM(tim, freq=500000, duty=0, pin=board_info.LED_R)
cnt=0
while(True):
    duty_val=math.fabs(math.sin(cnt))*100
    PWM_ch.duty(duty_val)
    cnt=cnt+0.01
    time.sleep_ms(1)
