## Copyright (c) 2019 aNoken
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

#Maixpyの特定versionでmobilenetv1 1000-Class が読めない場合があります。
#task = kpu.load("mbnet751.kmodel") or task = kpu.load(0x200000)
# SYSCALL: Out of memory
# ValueError: [MAIXPY]kpu: load error:6
# が発生。
#○:maixpy_v0.4.0_44_g95f00f0
#○:maixpy_v0.4.0_47_g39bb8bf
#×:maixpy_v0.4.0_49_g8279a1f
#×:maixpy_v0.4.0_82_gc3327b5
#https://github.com/sipeed/MaixPy/issues/180

import sensor, image, lcd, time
import KPU as kpu
lcd.init()
lcd.rotation(2)
lcd.clear()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)
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
    a = lcd.display(img)
    lcd.draw_string(10, 96, "%.2f:%s"%(pmax, labels[max_index].strip()))
    print(fps)
a = kpu.deinit(task)
