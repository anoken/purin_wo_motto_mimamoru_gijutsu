## Copyright (c) 2019 aNoå§ ÉvÉäÉìÇÇ‡Ç¡Ç∆å©éÁÇÈãZèp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from machine import I2C

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


# FIFO reset
i2c.writeto_mem(SH200I_ADDRESS, SH200I_FIFO_CONFIG, bytearray([0]));

# Chip ID default=0x18
tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0x30, 1);
print ("ChipID:", tempdata);
print(type(tempdata));

#sh200i_ADCReset
tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_ADC_RESET, 1);
print(tempdata);

tempdata = tempdata[0] | 0x04
i2c.writeto_mem(SH200I_ADDRESS, SH200I_ADC_RESET, bytearray([tempdata]));

tempdata = tempdata & 0xFB
i2c.writeto_mem(SH200I_ADDRESS, SH200I_ADC_RESET, bytearray([tempdata]));


tempdata = i2c.readfrom_mem(SH200I_ADDRESS, 0xD8, 1)
tempdata = tempdata[0] | 0x80
i2c.writeto_mem(SH200I_ADDRESS, 0xD8, bytearray([tempdata]));
time.sleep_ms(1)

tempdata = tempdata & 0x7F;
i2c.writeto_mem(SH200I_ADDRESS, 0xD8, bytearray([tempdata]));

tempdata=0x61
i2c.writeto_mem(SH200I_ADDRESS, 0x78, bytearray([tempdata]));
time.sleep_ms(1)

tempdata=0x00
i2c.writeto_mem(SH200I_ADDRESS, 0x78, bytearray([tempdata]));

#set acc odr 256hz
tempdata=0x91   #   0x81 1024hz   //0x89 512hz    //0x91  256hz
i2c.writeto_mem(SH200I_ADDRESS, SH200I_ACC_CONFIG, bytearray([tempdata]));

# set gyro odr 500hz
tempdata = 0x13; #0x11 1000hz    //0x13  500hz   //0x15  256hz
i2c.writeto_mem(SH200I_ADDRESS, SH200I_GYRO_CONFIG, bytearray([tempdata]));

# set gyro dlpf 50hz
tempdata = 0x03; #0x00 250hz   //0x01 200hz   0x02 100hz  0x03 50hz  0x04 25hz
i2c.writeto_mem(SH200I_ADDRESS, SH200I_GYRO_DLPF, bytearray([tempdata]));

# set no buffer mode
tempdata = 0x00;
i2c.writeto_mem(SH200I_ADDRESS, SH200I_FIFO_CONFIG, bytearray([tempdata]));

# set acc range +-8G
tempdata = 0x01;
i2c.writeto_mem(SH200I_ADDRESS, SH200I_ACC_RANGE, bytearray([tempdata]));

# set gyro range +-2000DPS/s
tempdata = 0x00;
i2c.writeto_mem(SH200I_ADDRESS, SH200I_GYRO_RANGE, bytearray([tempdata]));

tempdata = 0xC0;
i2c.writeto_mem(SH200I_ADDRESS, SH200I_REG_SET1, bytearray([tempdata]));

tempdata = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_REG_SET2, 1)

tempdata = tempdata[0] | 0x10
# ADC Reset
i2c.writeto_mem(SH200I_ADDRESS, SH200I_REG_SET2, bytearray([tempdata]));
time.sleep_ms(1)

tempdata = tempdata | 0xEF
i2c.writeto_mem(SH200I_ADDRESS, SH200I_REG_SET2, bytearray([tempdata]));
time.sleep_ms(10)

aRes = 8.0/32768.0;
gRes = 2000.0/32768.0;
while True:
    time.sleep_ms(200)

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

    accel_array = [accel_x*aRes, accel_y*aRes, accel_z*aRes]
    time.sleep_ms(10)

    gyro = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_OUTPUT_GYRO, 6)
    gyro_x = (gyro[1]<<8|gyro[0]);
    gyro_y = (gyro[3]<<8|gyro[2]);
    gyro_z = (gyro[5]<<8|gyro[4]);
    if gyro_x>32768:
        gyro_x=gyro_x-65536
    if gyro_y>32768:
        gyro_y=gyro_y-65536
    if gyro_z>32768:
        gyro_z=gyro_z-65536

    gyro_array = [gyro_x*gRes, gyro_y*gRes, gyro_z*gRes]
    print(gyro);

    print(accel_array,"_",gyro_array);

    temp = i2c.readfrom_mem(SH200I_ADDRESS, SH200I_OUTPUT_TEMP, 2)
    temp_dat = (temp[1]<<8| temp[0]) / 333.87 + 21.0

    print(temp_dat);




