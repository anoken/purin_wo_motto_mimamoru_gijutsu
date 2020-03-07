## Copyright (c) 2019 aNoken

import image, lcd, sensor,gc
from fpioa_manager import fm,board_info
import KPU as kpu
from Maix import GPIO
from pmu import axp192
from machine import UART,I2C
import ulab as np
from modules import ws2812

def update(capture,new_data,weight):
    new_data= new_data*weight+capture*(1.0-weight)
    return new_data

def get_dis(new_data,master_data):
    dist = np.sum((new_data-master_data)*(new_data-master_data))
    return dist

#M5StickV LCD Initialize
def m5stickv_init(uniV_use):
    if uniV_use==0:
        lcd.init()
        lcd.rotation(2)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    sensor.run(1)
    if uniV_use==0:
        pmu = axp192()
        pmu.setScreenBrightness(9)

def unitv_check():
    uniV_use=0
    i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
    devices = i2c.scan()
    if len(devices)==0:
        uniV_use=1
    return uniV_use


print("Initialize")
uniV_use=unitv_check()
m5stickv_init(uniV_use)

if uniV_use==1:
    class_ws2812 = ws2812(8,1)
    class_ws2812.set_led(0,(0,0,0))
    class_ws2812.display()

print("M5 Button def")
but_a_pressed = 0
but_b_pressed = 0

if uniV_use==0:
    fm.register(36, fm.fpioa.GPIO1)
    fm.register(37, fm.fpioa.GPIO2)
else :
    fm.register(18, fm.fpioa.GPIO1)
    fm.register(19, fm.fpioa.GPIO2)

but_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)


#UART Connection
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

task = kpu.load(0x200000)
#task = kpu.load("mobilenet_05.kmodel")
set=kpu.set_layers(task,29)

w_data=0.99
cap_weight=0.5

dummyImage = image.Image()
dummyImage = dummyImage.resize(32, 16)
kpu_dat = dummyImage.to_grayscale(1)

##Initial Value
img = sensor.snapshot()
fmap = kpu.forward(task, img)
new_data = np.array(fmap[:])
master_data = new_data

dist_old=0.0
img_buf = image.Image()

data_packet = bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

dist_thresh=100

while(True):
    #print(kpu.memtest())

    img = sensor.snapshot()
    fmap = kpu.forward(task, img)
    capture = np.array(fmap[:])
    new_data=update(capture,new_data,cap_weight)
    dist=get_dis(new_data,master_data)
    master_data=update(new_data,master_data,w_data)

    for row in range(32):
        for col in range(16):
            kpu_dat[16*row+col] = int(new_data[row*16+col]*100)

    if dist > dist_thresh:
        if uniV_use==1:
            class_ws2812.set_led(0,(1,0,0))
            class_ws2812.display()

        if dist_old <= dist_thresh:
            img_buf = img.copy()
            img_buf.compress(quality=70)
            img_size1 = (img_buf.size()& 0xFF0000)>>16
            img_size2 = (img_buf.size()& 0x00FF00)>>8
            img_size3 = (img_buf.size()& 0x0000FF)>>0
            data_packet = bytearray([0xFF,0xF1,0xF2,0xA1,img_size1,img_size2,img_size3,0x00,0x00,0x00])
            uart_Port.write(data_packet)
            uart_Port.write(img_buf)
            time.sleep(1.0)
            print("image send,data_packet")
        img.draw_rectangle(0,0,220,220,color = (255, 0, 0),thickness=10)
    else:
        if uniV_use==1:
            class_ws2812.set_led(0,(0,1,0))
            class_ws2812.display()

    dist_out = int(dist)
    dist_1 = (dist_out& 0x00FF00)>>8
    dist_2 = (dist_out& 0x0000FF)>>0
    dist_th1 = (dist_thresh& 0x00FF00)>>8
    dist_th2 = (dist_thresh& 0x0000FF)>>0

    data_packet = bytearray([0xFF,0xF3,0xF4,0xA1,dist_1,dist_2,dist_th1,dist_th2,0x00,0x00])
    uart_Port.write(data_packet)
    print("send",dist_out,"buf",data_packet)
    if dist <= dist_thresh:
        img.draw_rectangle(0,0,220,220,color = (0, 0, 255),thickness=10)

    if but_a.value() == 0 and but_a_pressed == 0:
        master_data = new_data
        but_a_pressed=1
        print("but_a_pressed")

    if but_a.value() == 1 and but_a_pressed == 1:
        but_a_pressed=0


    if but_b.value() == 0 and but_b_pressed == 0:
        dist_thresh+=25
        if dist_thresh>300:
            dist_thresh=25
        but_b_pressed=1

        print("but_b_pressed",dist_thresh)

    if but_b.value() == 1 and but_b_pressed == 1:
        but_b_pressed=0

    if uniV_use==0:
        lcd.draw_string(10, 0, "%.0f "%(dist), lcd.RED, lcd.BLACK)
        lcd.draw_string(30, 0, "/%.0f "%(dist_thresh), lcd.RED, lcd.BLACK)
        img2=img.resize(110,110)
        img3=kpu_dat.resize(60,60)
        lcd.display(img2,oft=(40,16))
        lcd.display(img3,oft=(160,41))
    dist_old=dist


