## Copyright (c) 2019 aNoken
## https://twitter.com/anoken2017

import sensor, image, time,lcd,machine,utime,array,math,os
from machine import I2C,UART
import KPU as kpu
from Maix import I2S, GPIO
import audio

# I2C Check
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print(devices)

lcd.init()

devices = os.listdir("/")
os.chdir("/sd")
print(os.listdir())


#################### Speaker
fm.register(board_info.SPK_SD, fm.fpioa.GPIO0)
spk_sd=GPIO(GPIO.GPIO0, GPIO.OUT)
spk_sd.value(1)
fm.register(board_info.SPK_DIN,fm.fpioa.I2S0_OUT_D1)
fm.register(board_info.SPK_BCLK,fm.fpioa.I2S0_SCLK)
fm.register(board_info.SPK_LRCLK,fm.fpioa.I2S0_WS)
wav_dev = I2S(I2S.DEVICE_0)

def play_wav(fname):
    player = audio.Audio(path = fname)
    player.volume(70)
    wav_info = player.play_process(wav_dev)
    wav_dev.channel_config(wav_dev.CHANNEL_1,
        I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT,
        align_mode = I2S.STANDARD_MODE)
    wav_dev.set_sample_rate(wav_info[1])
    while True:
        ret = player.play()
        if ret == None:
            break
        elif ret==0:
            break
    player.finish()

####################LCD_draw_face
x_zero=240//2
y_zero=135//2
x_zero_rot=x_zero
y_zero_rot=y_zero+0

def rot(x_in,y_in,theta):
    x_rot = (x_in - x_zero) * math.cos(theta)-  (y_in - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot = (x_in - x_zero) * math.sin(theta)        +  (y_in - y_zero) * math.cos(theta) + y_zero_rot;
    return int(x_rot),int(y_rot)

def rot2(x_in1,y_in1,x_in2,y_in2,theta):
    x_rot1 = (x_in1 - x_zero) * math.cos(theta)        - (y_in1 - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot1 = (x_in1 - x_zero) * math.sin(theta)        +  (y_in1 - y_zero) * math.cos(theta) + y_zero_rot;
    x_rot2 = (x_in2 - x_zero) * math.cos(theta)        - (y_in2 - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot2 = (x_in2 - x_zero) * math.sin(theta)        +  (y_in2 - y_zero) * math.cos(theta) + y_zero_rot;
    return int(x_rot1),int(y_rot1),int(x_rot2),int(y_rot2)

def draw_face(img,theta,cnt):
    img.draw_rectangle(0,0,240,135,color = (255, 255, 0), fill = True)
    if cnt<20:
        res = rot(70,70,theta)  #left_eye
        img.draw_circle(res[0], res[1], 32, color = (0, 0, 0),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (255, 255, 255),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 20, color = (0, 0, 0),            thickness = 2, fill = True)
        res = rot(170,70,theta) #right_eye
        img.draw_circle(res[0], res[1], 32, color = (0, 0, 0),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (255, 255, 255),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 20, color = (0, 0, 0),            thickness = 2, fill = True)
    else :
        res = rot2(40,70,80,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 10)
        res = rot2(160,70,200,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 10)

    res = rot2(160,30,200,10,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 15)
    res = rot2(80,30,40,10,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 15)

####################
# LCD Backlight
AXP192_ADDR=0x34
Backlight_ADDR=0x91
level=50
val = (level+7) << 4
i2c.writeto_mem(AXP192_ADDR, Backlight_ADDR,int(val))
####################

# IMU6866 define
MPU6886_ADDRESS=0x68
MPU6886_WHOAMI=0x75
MPU6886_ACCEL_INTEL_CTRL=  0x69
MPU6886_SMPLRT_DIV=0x19
MPU6886_INT_PIN_CFG=   0x37
MPU6886_INT_ENABLE=0x38
MPU6886_ACCEL_XOUT_H=  0x3B
MPU6886_TEMP_OUT_H=0x41
MPU6886_GYRO_XOUT_H=   0x43
MPU6886_USER_CTRL= 0x6A
MPU6886_PWR_MGMT_1=0x6B
MPU6886_PWR_MGMT_2=0x6C
MPU6886_GYRO_CONFIG=   0x1B
MPU6886_ACCEL_CONFIG=  0x1C
MPU6886_ACCEL_CONFIG2= 0x1D
MPU6886_FIFO_EN=   0x23
MPU6886_CONFIG=0x1A

# IMU6866 Initialize
def write_i2c(address, value):
    i2c.writeto_mem(MPU6886_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

write_i2c(MPU6886_PWR_MGMT_1, 0x00)
write_i2c(MPU6886_PWR_MGMT_1, 0x01<<7)
write_i2c(MPU6886_PWR_MGMT_1,0x01<<0)
write_i2c(MPU6886_ACCEL_CONFIG,0x10)
write_i2c(MPU6886_GYRO_CONFIG,0x18)
write_i2c(MPU6886_CONFIG,0x01)
write_i2c(MPU6886_SMPLRT_DIV,0x05)
write_i2c(MPU6886_INT_ENABLE,0x00)
write_i2c(MPU6886_ACCEL_CONFIG2,0x00)
write_i2c(MPU6886_USER_CTRL,0x00)
write_i2c(MPU6886_FIFO_EN,0x00)
write_i2c(MPU6886_INT_PIN_CFG,0x22)
write_i2c(MPU6886_INT_ENABLE,0x01)

####################

# Button_A
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

# Button_B
fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0


# Read IMU6866 and Scaling
def read_imu():
    aRes=255/8192/2
    offset=128
    accel = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_ACCEL_XOUT_H, 6)
    accel_x = (accel[0]<<8|accel[1])
    accel_y = (accel[2]<<8|accel[3])
    accel_z = (accel[4]<<8|accel[5])
    if accel_x>32768:
        accel_x=accel_x-65536
    if accel_y>32768:
        accel_y=accel_y-65536
    if accel_z>32768:
        accel_z=accel_z-65536
    ax=int(accel_x*aRes+offset)
    if ax<0: ax=0
    if ax>255: ax=255
    ay=int(accel_y*aRes+offset)
    if ay<0: ay=0
    if ay>255: ay=255
    az=int(accel_z*aRes+offset)
    if az<0: az=0
    if az>255: az=255
    accel_array = [ay,az,ax]
    accel_array2 = [accel_x,accel_y,accel_z]
    return accel_array,accel_array2

cnt=0
mode=0
view_flg=0
pic_no=0
accel_array_zero=(255,255,255)

#IMU_Image
w_size=8
view_size=120
imu_Image = image.Image()
imu_Image = imu_Image.resize(w_size, w_size)
image_data_array = []

task = kpu.load(0x00300000)
max_index=0
view_mode=0

class_time=array.array('d',[0 for ii in range(10)])
oldTime = utime.ticks_ms()
rot_theta=0

#uart initial
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

while(True):
    view_Image = image.Image()

    # IMU Data to Image
    accel_array,accel_array2 = read_imu()
    w=cnt%w_size
    h=int(cnt/w_size)
    imu_Image.set_pixel(w, h, accel_array)
    width=imu_Image.width()

    # IMU Data_View
    w=(cnt+1)%w_size
    h=int((cnt+1)/w_size)
    imu_Image.set_pixel(w, h, accel_array_zero)
    img_buff=imu_Image.resize(view_size,view_size)
    view_Image.draw_image(img_buff,100,8)

    class_str=str(max_index);
    view_Image.draw_string(20, 40, "ACT", (0,0,255),scale=2)
    view_Image.draw_string(20, 70,class_str, (0,0,255),scale=5)

    if cnt%width<width/2:
        view_Image.draw_circle(30, 15, 15,(0,0,255),fill=1)

    rot_theta=0.5*rot_theta+0.5*math.atan2(accel_array2[1], accel_array2[0])
    face_img = image.Image()
    draw_face(face_img,rot_theta,cnt)
    face_img.draw_string(0, 80, "ACT", (0,0,255),scale=2)
    face_img.draw_string(0, 90,class_str, (0,0,255),scale=5)


    if view_mode==0:
        lcd.display(face_img)
    elif view_mode==1:
        lcd.display(view_Image)

    cnt=cnt+1

    # IMU Data to KPU
    if cnt>imu_Image.width()*imu_Image.height():
        cnt=0
        imu_Image.pix_to_ai()
        fmap=kpu.forward(task,imu_Image)
        plist=fmap[:]
        pmax=max(plist)
        max_index=plist.index(pmax)
        dT=utime.ticks_ms()-oldTime
        class_time[max_index]=class_time[max_index]+dT/1000
        oldTime = utime.ticks_ms()

        for i in range(10):
            moji=str("No")+str(i)+str("_")+str(class_time[i])+str("_")
            print(moji, end='')
        print("")

        #send uart
        data_str=str(max_index)+"\n"
        uart_Port.write(data_str)

    if class_time[0]>20:
        play_wav("voice/okite.wav")
        class_time[0]=0

    if class_time[1]>20:
        play_wav("voice/sumaho.wav")
        class_time[1]=0

    if class_time[2]>20:
        play_wav("voice/ganbare.wav")
        class_time[2]=0
        
    if class_time[3]>20:
        play_wav("voice/ganbare.wav")
        class_time[3]=0
        
    if but_a.value() == 0 and but_a_pressed == 0:
        but_a_pressed=1

    if but_a.value() == 1 and but_a_pressed == 1:
        but_a_pressed=0

    if but_b.value() == 0 and but_b_pressed == 0:
        but_b_pressed=1
        if view_mode==0:
            view_mode=1
        elif view_mode==1:
            view_mode=0

    if but_b.value() == 1 and but_b_pressed == 1:
        but_b_pressed=0
