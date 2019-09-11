## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import network, socket, sensor, image, lcd
from Maix import GPIO
from fpioa_manager import fm, board_info
from machine import UART

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0


while True:
    img = sensor.snapshot()
    lcd.display(img)
    if but_a.value() == 0 and but_a_pressed == 0:
        img_buf = img.compress(quality=70)
        img_size1 = (img.size()& 0xFF0000)>>16
        img_size2 = (img.size()& 0x00FF00)>>8
        img_size3 = (img.size()& 0x0000FF)>>0
        data_packet = bytearray([0xFF,0xD8,0xEA,0x01,
        img_size1,img_size2,img_size3,0x00,0x00,0x00])
        uart_Port.write(data_packet)
        uart_Port.write(img_buf)
        time.sleep(1.0)
        but_a_pressed=1
    if but_a.value() == 1 and but_a_pressed == 1:
        but_a_pressed=0

uart_Port.deinit()
del uart_Port
