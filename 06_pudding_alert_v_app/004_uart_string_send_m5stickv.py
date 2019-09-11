## Copyright (c) 2019 aNoken 
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from Maix import GPIO
from fpioa_manager import fm, board_info
from machine import UART

fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
cnt=0
while True:
    moji=str(cnt)+"\n"
    uart_Port.write(moji)
    time.sleep(1.0)
    cnt=cnt+1

uart_Port.deinit()
del uart_Port