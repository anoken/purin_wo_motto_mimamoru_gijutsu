## Copyright (c) 2019 aNoå§ ÉvÉäÉìÇÇ‡Ç¡Ç∆å©éÁÇÈãZèp 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import lcd,math,image
lcd.init()
lcd.rotation(2)
lcd.clear()
x_zero=240//2
y_zero=135//2
x_zero_rot=x_zero
y_zero_rot=y_zero+90

def rot(x_in,y_in,theta):
    x_rot = (x_in - x_zero) * math.cos(theta)  - (y_in - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot = (x_in - x_zero) * math.sin(theta) +  (y_in - y_zero) * math.cos(theta) + y_zero_rot;
    return int(x_rot),int(y_rot)

def rot2(x_in1,y_in1,x_in2,y_in2,theta):
    x_rot1 = (x_in1 - x_zero) * math.cos(theta)  - (y_in1 - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot1 = (x_in1 - x_zero) * math.sin(theta)  +  (y_in1 - y_zero) * math.cos(theta) + y_zero_rot;
    x_rot2 = (x_in2 - x_zero) * math.cos(theta)  - (y_in2 - y_zero) * math.sin(theta) + x_zero_rot;
    y_rot2 = (x_in2 - x_zero) * math.sin(theta)  +  (y_in2 - y_zero) * math.cos(theta) + y_zero_rot;
    return int(x_rot1),int(y_rot1),int(x_rot2),int(y_rot2)
    
def draw_face(img,theta,cnt):
    img.draw_rectangle(0,0,240,135,color = (255, 255, 0), fill = True)
    if cnt<100:
        res = rot(40,70,theta)  #left_eye
        img.draw_circle(res[0], res[1], 42, color = (0, 0, 0),
            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 40, color = (255, 255, 255), 
            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (0, 0, 0),
            thickness = 2, fill = True)
        res = rot(200,70,theta) #right_eye
        img.draw_circle(res[0], res[1], 42, color = (0, 0, 0), 
            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 40, color = (255, 255, 255),
            thickness = 2, fill = True)
        img.draw_circle(res[0], res[1], 30, color = (0, 0, 0), 
            thickness = 2, fill = True)
    else :
        res = rot2(10,70,80,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0), 
            thickness = 10)
        res = rot2(170,70,250,70,theta)
        img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0), 
            thickness = 10)

    res = rot2(170,10,240,-20,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0),
            thickness = 15)
    res = rot2(70,10,0,-20,theta)
    img.draw_line(res[0], res[1], res[2], res[3], color = (0, 0, 0), 
            thickness = 15)

rot_theta=3.1415/2*3
cnt=0
while True:
    img = image.Image()
    draw_face(img,rot_theta,cnt)
    lcd.display(img)
    cnt+=1
    if cnt>200:
        cnt=0
    rot_theta=rot_theta+0.05
