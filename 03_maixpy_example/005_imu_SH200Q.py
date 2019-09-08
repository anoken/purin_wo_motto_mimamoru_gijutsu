## Copyright (c) 2019 aNoå§ ÉvÉäÉìÇÇ‡Ç¡Ç∆å©éÁÇÈãZèp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from machine import I2C
import lcd

i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print("i2c",devices)

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

def write_i2c(address, value):
    i2c.writeto_mem(SH200I_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

def SH200I_init():
    # FIFO reset
    write_i2c(SH200I_FIFO_CONFIG, 0x00)
    # Chip ID default=0x18
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0x30, 1);
    print ("ChipID:", tempdata);

    #sh200i_ADCReset
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_ADC_RESET, 1);
    tempdata = tempdata[0] | 0x04
    write_i2c(SH200I_ADC_RESET, tempdata)
    tempdata = tempdata & 0xFB
    write_i2c(SH200I_ADC_RESET, tempdata)
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0xD8, 1)
    tempdata = tempdata[0] | 0x80
    write_i2c(0xD8, tempdata)
    tempdata = tempdata & 0x7F;
    write_i2c(0xD8, tempdata)
    write_i2c(0x78, 0x61)
    write_i2c(0x78, 0x00)
    #set acc odr 256hz
    #   0x81 1024hz   //0x89 512hz    //0x91  256hz
    write_i2c(SH200I_ACC_CONFIG, 0x91)
    # set gyro odr 500hz
    #0x11 1000hz    //0x13  500hz   //0x15  256hz
    write_i2c(SH200I_GYRO_CONFIG, 0x13)
    # set gyro dlpf 50hz
    #0x00 250hz   //0x01 200hz   0x02 100hz  0x03 50hz  0x04 25hz
    write_i2c(SH200I_GYRO_DLPF, 0x03)
    # set no buffer mode
    write_i2c(SH200I_FIFO_CONFIG, 0x00)
    # set acc range +-8G
    write_i2c(SH200I_ACC_RANGE, 0x01)
    # set gyro range +-2000DPS/s
    write_i2c(SH200I_GYRO_RANGE, 0x00)
    tempdata = 0xC0;
    write_i2c(SH200I_REG_SET1, 0xC0)
    tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_REG_SET2, 1)
    tempdata = tempdata[0] | 0x10
    # ADC Reset
    write_i2c(SH200I_REG_SET2, tempdata)
    tempdata = tempdata | 0xEF
    write_i2c(SH200I_REG_SET2, tempdata)

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

SH200I_init()
lcd.init()
lcd.clear()
aRes = 8.0/32768.0;
while True:
    x,y,z=SH200I_acc_read()
    accel_array = [x*aRes, y*aRes, z*aRes]
    print(accel_array);
    lcd.draw_string(20,50,"x:"+str(accel_array[0]))
    lcd.draw_string(20,70,"y:"+str(accel_array[1]))
    lcd.draw_string(20,90,"z:"+str(accel_array[2]))
    time.sleep_ms(10)


