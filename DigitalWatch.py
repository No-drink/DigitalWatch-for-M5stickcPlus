from m5stack import *
from m5ui import *
from uiflow import *
import imu
import time
from easyIO import *

setScreenColor(0x111111)


s = None
h = None
m = None
sel=None
light=None
imu0 = None
angle=None
b=None


label0 = M5TextBox(109, 30, "hour", lcd.FONT_Default, 0xFFFFFF, rotate=90)
label1 = M5TextBox(109, 90, "minute", lcd.FONT_Default, 0xFFFFFF, rotate=90)
label2 = M5TextBox(109, 159, "second", lcd.FONT_Default, 0x00dc21, rotate=90)
HH = M5TextBox(72, 20, "00", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=90)
MM = M5TextBox(72, 90, "00", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=90)
SS = M5TextBox(72, 159, "00", lcd.FONT_DejaVu40, 0x00dc21, rotate=90)
rectangle0 = M5Rect(0, 0, 5, 33, 0x0bff00, 0x0bff00)
rectangle1 = M5Rect(130, 0, 5, 33, 0xff0000, 0xff0000)

from numbers import Number


# Describe this function...
def update_display():
  global s, h, m
  if s > 59:
    s = 0
    m = (m if isinstance(m, Number) else 0) + 1
  if m > 59:
    m = 0
    h = (h if isinstance(h, Number) else 0) + 1
  if h > 23:
    h = 0
  if s >= 10:
    SS.setText(str(s))
  else:
    SS.setText(str((str('0') + str(s))))
  if m >= 10:
    MM.setText(str(m))
  else:
    MM.setText(str((str('0') + str(m))))
  if h >= 10:
    HH.setText(str(h))
  else:
    HH.setText(str((str('0') + str(h))))
    
  if sel==0:
    SS.setColor(0xf70000)
    MM.setColor(0xFFFFFF)
    HH.setColor(0xFFFFFF)
  elif sel==1:
    SS.setColor(0x00dc21)
    MM.setColor(0xf70000)
    HH.setColor(0xFFFFFF)
  elif sel==2:
    SS.setColor(0x00dc21)
    MM.setColor(0xFFFFFF)
    HH.setColor(0xf70000)
  elif sel==3:
    SS.setColor(0x00dc21)
    MM.setColor(0xFFFFFF)
    HH.setColor(0xFFFFFF)
    
  
  if light==1 or (light==0 and angle==1):
    axp.setLcdBrightness(50)
  else:
    axp.setLcdBrightness(0)
  

  rectangle0.setSize(height=(s * 4))
  rectangle1.setSize(height=int(b * 2.40))


@timerSch.event('seconds')
def tseconds():
  global s, h, m
  s = (s if isinstance(s, Number) else 0) + 1
  update_display()
  pass


h = rtc.now()[3]
m = rtc.now()[4]
s = rtc.now()[5]
sel=3
light=1
imu0 = imu.IMU()
angle=0
lock=0
b=0
timerSch.run('seconds', 1000, 0x00)

while True:
  b = map_value((axp.getBatVoltage()), 3.7, 4.1, 0, 100)
  if light==0:
    if -30<imu0.ypr[1]<30 and -50<imu0.ypr[2]<10 :
      angle=1
    else :
      angle=0

  if btnB.isPressed():
    sel= sel + 1
    sel=sel%4
    if sel !=3:
      light=1
    wait_ms(50)
    if sel==0:
      speaker.tone(1800, 200)
    elif sel==1:
      speaker.tone(1800, 200)
    elif sel==2:
      speaker.tone(1800, 200)
    elif sel==3:
      speaker.tone(1800, 200)
      M5Led.on()
      wait_ms(50)
      M5Led.off()
      wait_ms(50)
      speaker.tone(1800, 200)
      M5Led.on()
      wait_ms(50)
      M5Led.off()


  if btnA.isPressed() and sel==0:
    s = (s if isinstance(s, Number) else 0) + 1
    wait_ms(50)
  elif   btnA.isPressed() and sel==1:
    m = (m if isinstance(m, Number) else 0) + 1
    wait_ms(50)
  elif   btnA.isPressed() and sel==2:
    h = (h if isinstance(h, Number) else 0) + 1
    wait_ms(50)
  elif   btnA.isPressed() and sel==3:
    light=light+1
    light=light%3
    speaker.tone(1800, 200)
    wait_ms(200)

  update_display()

  wait_ms(2)
