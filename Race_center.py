

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) 
import time
from threading import Thread

import RPLCD

import Port_IO as p
import globals as g

g.Anzahl_Spuren = len(p.SEN)

g.global_init()

if g.english == False:
	import Anzeige_de as a
else:
	import Anzeige_en as a

import Tools as t
t.Tools_init()

t.Buzzer_out(0.1)

import Keyhandler as k
k.Key_init()



for i in range(0,16):
	t.LED_off(i)						

g.Boot_time = time.time()


# check for vehicle in start position and set LED
for i in  p.SEN:
	if GPIO.input(i)==True: #kein Fahrzeug. 
		g.Sensor_list[p.SEN.index(i)]=True
		t.LED_off(p.LED_W[p.SEN.index(i)])
	
	else: 
		g.Sensor_list[p.SEN.index(i)] = False    #vehicle present
		t.LED_W_on(p.LED_W[p.SEN.index(i)])	


s = Thread(target=t.my_timer)     #separate timer function, because system time can change after accessing network (internet)
s.start()


d = Thread(target=a.Anzeige)  #Anzeige (Display) loop
d.start()






#from subprocess import call

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print()

except:
	print()

finally:
#	GPIO.cleanup() # this ensures a clean exit 
	i=1

