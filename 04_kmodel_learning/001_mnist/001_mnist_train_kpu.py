import sensor,lcd,image
import KPU as kpu
lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
task = kpu.load("mnist.kmodel")
sensor.run(1)
while True:
    img = sensor.snapshot()
    lcd.display(img)              
    img1=img.to_grayscale(1)     
    img2=img1.resize(28,28)       
    a=img2.invert()                
    a=img2.strech_char(1)           
    lcd.display(img2,oft=(120,32))
    a=img2.pix_to_ai();           
    fmap=kpu.forward(task,img2)	
    plist=fmap[:]                 
    pmax=max(plist)               
    max_index=plist.index(pmax)	
    lcd.draw_string(0,0,"%d: %.3f"%(max_index,pmax),lcd.WHITE,lcd.BLACK)