"""1. 서브 모터 +LED 색변환"""

from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")

while(True):
    rs.set_rgb_led_on(3)
    rs.servo_write(2,90)
    rs.set_rgb_led_red(3)
    rs.delay(1)
    rs.servo_write(2,0)
    rs.set_rgb_led_yellow(3)
    rs.delay(1)
    rs.servo_write(2,-90)
    rs.set_rgb_led_green(3)
    rs.delay(1)


"""
2. 서브모터 + LED 색변환 + 도레미
from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""

while(True):
    rs.set_rgb_led_on(3)
    rs.servo_write(2,90)
    rs.set_rgb_led_red(3)
    rs.tone(4,60,170)
    rs.delay(1)
    rs.servo_write(2,0)
    rs.set_rgb_led_yellow(3)
    rs.tone(4,62,170)
    rs.delay(1)
    rs.servo_write(2,-90)
    rs.set_rgb_led_green(3)
    rs.tone(4,64,170)
    rs.delay(1)


"""
3. 서브모터 + LED 색변환 + 도레미파솔파미레도
from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""

while(True):
    rs.set_rgb_led_on(3)
    rs.delay(1)
    rs.servo_write(2,90)
    rs.set_rgb_led_red(3)
    rs.tone(4,60,170)
    rs.delay(1)
    rs.servo_write(2,45)
    rs.set_rgb_led_orange(3)
    rs.tone(4,62,170)
    rs.delay(1)
    rs.servo_write(2,0)
    rs.set_rgb_led_yellow(3)
    rs.tone(4,64,170)
    rs.delay(1)
    rs.servo_write(2,-45)
    rs.set_rgb_led_green(3)
    rs.tone(4,65,170)
    rs.delay(1)
    rs.servo_write(2,-90)
    rs.set_rgb_led_purple(3)
    rs.tone(4,67,170)
    rs.delay(1)
    rs.servo_write(2,-45)
    rs.set_rgb_led_pink(3)
    rs.tone(4,65,170)
    rs.delay(1)
    rs.servo_write(2,0)
    rs.set_rgb_led_white(3)
    rs.tone(4,64,170)
    rs.delay(1)
    rs.servo_write(2,45)
    rs.set_rgb_led_sky(3)
    rs.tone(4,62,170)
    rs.delay(1)
    rs.servo_write(2,90)
    rs.set_rgb_led_red(3)
    rs.tone(4,60,170)
    rs.delay(1)

"""
4. LED+초음파센서 (실시간 data 나오게 설정)

from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""
rs.sonar_begin(6)

 while(True):
    data = rs.sonar_read(6)
    print("data:",  data)
    if data >= 2 and data <= 5:
        rs.set_rgb_led_red(3)
        rs.set_rgb_led_on(3)
  
        
    elif data >= 6 and data <=10:
        rs.set_rgb_led_orange(3)
        rs.set_rgb_led_on(3)

    elif data >= 11 and data <=15:
        rs.set_rgb_led_yellow(3)
        rs.set_rgb_led_on(3)

    elif data >= 16 and data <=20:
        rs.set_rgb_led_green(3)
        rs.set_rgb_led_on(3)

    elif data >= 21 and data <=30:
        rs.set_rgb_led_sky(3)
        rs.set_rgb_led_on(3)

    elif data >= 26 and data <=40:
        rs.set_rgb_led_pink(3)
        rs.set_rgb_led_on(3)    
    else:
        rs.set_rgb_led_off(3)
        rs.set_rgb_led_on(3)    




"""
5. 서브모터 + LED+ 초음파센서 (실시간 data 나오게 설정)

from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""

rs.sonar_begin(6)

 
while(True):
    data = rs.sonar_read(6)
    print("data:",  data)
    if data >= 2 and data <= 5:
        rs.set_rgb_led_red(3)
        rs.set_rgb_led_on(3)
        rs.servo_write(2,-90)
      
        
    elif data >= 6 and data <=10:
        rs.set_rgb_led_orange(3)
        rs.set_rgb_led_on(3)
        rs.servo_write(2,0)
     
    elif data >= 11 and data <=15:
        rs.set_rgb_led_yellow(3)
        rs.set_rgb_led_on(3)
        rs.servo_write(2,90)
    elif data >= 16 and data <=20:
        rs.set_rgb_led_green(3)
        rs.set_rgb_led_on(3)

    elif data >= 21 and data <=30:
        rs.set_rgb_led_sky(3)
        rs.set_rgb_led_on(3)

    elif data >= 26 and data <=40:
        rs.set_rgb_led_pink(3)
        rs.set_rgb_led_on(3)    
    else:
        rs.set_rgb_led_off(3)
        rs.set_rgb_led_on(3)    

"""
7. 메카넘힐 두 바퀴만 세번씩 돌리기
from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""

isCW = True
isCCW = False

loop = 0

while loop < 3:
    if isCW == True:
        rs.motor_write(0, 0, 15)
        rs.motor_write(2, 0, 15)

        rs.delay(3)
    

        isCW = False
        isCCW = True
        
                
    elif isCCW == True :
        rs.motor_write(0, 1, 15)
        rs.motor_write(2, 1, 15)
        rs.delay(3)
     
        
        isCW = True
        isCCW = False

        loop+=1

rs.motor_stop(0)
rs.motor_stop(2)
        
"""        
8. 대각선 방향 이동
from RobokitRS import *
rs = RobokitRS.RobokitRS()
rs.port_open("com3")
"""

rs.set_mecanumwheels_drive_frontleft(15,1)
rs.delay(1)
rs.set_mecanumwheels_drive_backright(15,1)
rs.delay(1)
rs.set_mecanumwheels_drive_frontright(15 ,1)
rs.delay(1)
rs.set_mecanumwheels_drive_backleft(15,1)
rs.delay(1)
rs.set_mecanumwheels_drive_stop(1)
	