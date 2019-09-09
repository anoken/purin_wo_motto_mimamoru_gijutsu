## Copyright (c) 2019 aNoå§ ÉvÉäÉìÇÇ‡Ç¡Ç∆å©éÁÇÈãZèp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from machine import I2C
import lcd,math,image

####################
## 019_LCD_draw_face.py
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
    if cnt<100:
        res = rot(40,70,theta)  #left_eye
        img.draw_circle(res[0], res[1], 42, color = (0, 0, 0),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 40, color = (255, 255, 255),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (0, 0, 0),            thickness = 2, fill = True)
        res = rot(200,70,theta) #right_eye
        img.draw_circle(res[0], res[1], 42, color = (0, 0, 0),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 40, color = (255, 255, 255),            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (0, 0, 0),            thickness = 2, fill = True)
    else :
        res = rot2(10,70,80,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 10)
        res = rot2(170,70,250,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 10)

    res = rot2(170,10,240,-20,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 15)
    res = rot2(70,10,0,-20,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),            thickness = 15)

####################
## 005_imu_SH200Q.py

SH200I_ADDRESS=108
SH200I_WHOAMI= 0x30
SH200I_ACC_CONFIG= 0x0E
SH200I_GYRO_CONFIG= 0x0F
SH200I_GYRO_DLPF= 0x11
SH200I_FIFO_CONFIG= 0x12
SH200I_ACC_RANGE= 0x16
SH200I_GYRO_RANGE= 0x2B
SH200I_OUTPUT_ACC= 0x00
SH200I_OUTPUT_GYRO= 0x06
SH200I_OUTPUT_TEMP= 0x0C
SH200I_REG_SET1= 0xBA
SH200I_REG_SET2= 0xCA   #ADC reset
SH200I_ADC_RESET=  0xC2   #drive reset
SH200I_SOFT_RESET= 0x7F
SH200I_RESET= 0x75

def write_i2c_sh200(address, value):
    i2c.writeto_mem(SH200I_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

def SH200I_init():
    # FIFO reset
    write_i2c_sh200(SH200I_FIFO_CONFIG, 0x00)
    # Chip ID default=0x18
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0x30, 1);
    print ("ChipID:", tempdata);

    #sh200i_ADCReset
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_ADC_RESET, 1);
    tempdata = tempdata[0] | 0x04
    write_i2c_sh200(SH200I_ADC_RESET, tempdata)
    tempdata = tempdata & 0xFB
    write_i2c_sh200(SH200I_ADC_RESET, tempdata)
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0xD8, 1)
    tempdata = tempdata[0] | 0x80
    write_i2c_sh200(0xD8, tempdata)
    tempdata = tempdata & 0x7F;
    write_i2c_sh200(0xD8, tempdata)
    write_i2c_sh200(0x78, 0x61)
    write_i2c_sh200(0x78, 0x00)
    #set acc odr 256hz
    #   0x81 1024hz   //0x89 512hz    //0x91  256hz
    write_i2c_sh200(SH200I_ACC_CONFIG, 0x91)
    # set gyro odr 500hz
    #0x11 1000hz    //0x13  500hz   //0x15  256hz
    write_i2c_sh200(SH200I_GYRO_CONFIG, 0x13)
    # set gyro dlpf 50hz
    #0x00 250hz   //0x01 200hz   0x02 100hz  0x03 50hz  0x04 25hz
    write_i2c_sh200(SH200I_GYRO_DLPF, 0x03)
    # set no buffer mode
    write_i2c_sh200(SH200I_FIFO_CONFIG, 0x00)
    # set acc range +-8G
    write_i2c_sh200(SH200I_ACC_RANGE, 0x01)
    # set gyro range +-2000DPS/s
    write_i2c_sh200(SH200I_GYRO_RANGE, 0x00)
    tempdata = 0xC0;
    write_i2c_sh200(SH200I_REG_SET1, 0xC0)
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_REG_SET2, 1)
    tempdata = tempdata[0] | 0x10
    # ADC Reset
    write_i2c_sh200(SH200I_REG_SET2, tempdata)
    tempdata = tempdata | 0xEF
    write_i2c_sh200(SH200I_REG_SET2, tempdata)

def SH200I_acc_read():
    accel = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_OUTPUT_ACC, 6)
    accel_x = (accel[1]<<8|accel[0]);
    accel_y = (accel[3]<<8|accel[2]);
    accel_z = (accel[5]<<8|accel[4]);
    if accel_x>32768:
        accel_x=accel_x-65536
    if accel_y>32768:
        accel_y=accel_y-65536
    if accel_z>32768:
        accel_z=accel_z-65536
    return accel_x,accel_y,accel_z

####################
## 006_imu_MPU6886.py

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
MPU6886_CONFIG=0x1A
MPU6886_GYRO_CONFIG=   0x1B
MPU6886_ACCEL_CONFIG=  0x1C
MPU6886_ACCEL_CONFIG2= 0x1D
MPU6886_FIFO_EN=   0x23

def write_i2c(address, value):
    i2c.writeto_mem(MPU6886_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

def MPU6866_init():
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

def MPU6866_read():
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
    return accel_x,accel_y,accel_z

#####################


lcd.init()
lcd.rotation(2)
lcd.clear()
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()

if devices==[52,108]: #SH200Q
    SH200I_init()
elif devices==[52,104]: #MPU6866
    MPU6866_init()

cnt=0
rot_theta=0
x=0
y=0
z=0
while True:
    if devices==[52,108]: #SH200Q
        x,y,z=SH200I_acc_read()
    elif devices==[52,104]: #MPU6866
        x,y,z=MPU6866_read()
    accel_array = [x, y, z]
    rot_theta=0.5*rot_theta-0.5*math.atan2(accel_array[1], -accel_array[0])
    img = image.Image()
    draw_face(img,rot_theta,cnt)
    lcd.display(img)
    cnt+=1
    if cnt>200:
        cnt=0
