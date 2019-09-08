## Copyright (c) 2019 aNo研 プリンをもっと見守る技術 
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

import sensor, image, lcd, time
import KPU as kpu
lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)
lcd.clear()
lcd.draw_string(100,96,"MobileNet Demo")
lcd.draw_string(100,112,"Loading labels...")
f=open('labels.txt','r')
labels=f.readlines()
f.close()
task = kpu.load("mbnet751.kmodel")
clock = time.clock()
while(True):
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    a = lcd.display(img, oft=(0,0))
    lcd.draw_string(0, 224, "%.2f:%s"%(pmax, labels[max_index].strip()))
    print(fps)
a = kpu.deinit(task)
