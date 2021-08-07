import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) 
import time

import Adafruit_PCA9685

import Port_IO as p
import globals as g

# Import the PCA9685 module.
LED = Adafruit_PCA9685.PCA9685(address=p.PWM_EXP)

# Set the PWM frequency to 60hz.

LED.frequency = 60

Flip = True #toggle LED after qualification/race is finished

def Sen_trig(channel,index):
	global g

	if GPIO.input(p.SEN[index])==True: #kein Fahrzeug. 
		g.Sensor_list[index]=True
		LED_off(p.LED_W[index])
	else: 
		g.Sensor_list[index] = False    #Fahrzeug erkannt; Zeitmessung bei Einfahrt in die Lichtschranke
		LED_W_on(p.LED_W[index])	
		if g.im_rennen == True and g.Track_in_use[index] == False:
			g.Fahrzeug_list[index].Anzahl_Runden += 1		
			if g.Rennen_Runden - g.Fahrzeug_list[index].Anzahl_Runden-g.Fahrzeug_list[index].Vorsprung<=0 and g.Statemachine == 30:
					g.gefahrene_Zeit = timer_time()
					g.im_rennen = False
					Fanfahre()		
			zeit = timer_time()
			g.Fahrzeug_list[index].Zeit_letzte_Runde = zeit - g.Fahrzeug_list[index].Zeit_Runde_Start
			if g.Fahrzeug_list[index].Zeit_letzte_Runde >99.99:
				g.Fahrzeug_list[index].Zeit_letzte_Runde = 99.99
			if g.Fahrzeug_list[index].Zeit_letzte_Runde < g.Fahrzeug_list[index].Zeit_beste_Runde:
				g.Fahrzeug_list[index].Zeit_beste_Runde = g.Fahrzeug_list[index].Zeit_letzte_Runde
			g.Fahrzeug_list[index].Zeit_Runde_Start = zeit
			
	print (index+1)
		
def Sen_LED_off(channel,index):
	global g
	LED_off(p.LED_W[index])

def Tools_init():
	global g
	global p
	for i in p.SEN:
		#print (str(i) + '  ' + str(p.SEN.index(i)))
		GPIO.setup(i, GPIO.IN) # Sensor 1
		GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		cb = lambda channel, arg1=p.SEN.index(i): Sen_trig(channel, arg1)

		GPIO.add_event_detect(i, GPIO.FALLING, callback = cb, bouncetime = g.Debounce) 

		if GPIO.input(i)==True: #kein Fahrzeug. "fallende" (logisch steigende) Flanke wird für Zeitmessung verwendet
			g.Sensor_list[p.SEN.index(i)]=True
			LED_off(p.LED_W[p.SEN.index(i)])
		
		else: 
			g.Sensor_list[p.SEN.index(i)] = False    #Fahrzeug erkannt
			LED_W_on(p.LED_W[p.SEN.index(i)])	
	GPIO.setup(p.Buzzer,GPIO.OUT)
	
def LED_on(port):   #LED ungedimmt
	LED.set_pwm(port, 0, 4096)	

def LED_W_on(port):
	LED.set_pwm(port, 0, int(4096/100*g.LED_W_dim))	

def LED_R_on(port):
	LED.set_pwm(port, 0, int(4096/100*g.LED_R_dim))	

def LED_G_on(port):
	LED.set_pwm(port, 0, int(4096/100*g.LED_G_dim))	

def LED_off(port):
	LED.set_pwm(port, 4096, 0)





def timer_time():
	global g
	return time.time() - g.Boot_time - g.time_jump


def check_time():
	global g
	if timer_time() - g.last_time > 10:  #time synchro with internet
		g.time_jump = timer_time() - g.last_time - 0.1
	g.last_time = timer_time()


def check_sens():
	global g
	for j in p.SEN:
		if GPIO.input(j)==True: #kein Fahrzeug.
			g.Sensor_list[p.SEN.index(j)]=True
			LED_off(p.LED_W[p.SEN.index(j)]) 
		
		


def Startampel():
#for i in range(90, 100):

	for j in range (0,5):
		LED_R_on(p.LED_R[j])
		LED_R_on(p.LED_R[j+5])
		time.sleep(1)

	for j in range(0,5):
		LED_off(p.LED_R[j])    
		LED_off(p.LED_R[j+5]) 


def init_race():
	global g
	temp = []
	for i in range(0,g.Anzahl_Spuren):
		temp.append(g.Fahrzeug_list[i].Vorsprung)
	g.Fahrzeug_list.clear()
	for i in range(0,g.Anzahl_Spuren):
		g.Fahrzeug_list.append(g.Fahrzeug(0.0,0.0,99.99,0,0))
		g.Fahrzeug_list[i].Vorsprung=temp[i]
		if g.Track_in_use[i] == True: #inverted logic!
			g.Fahrzeug_list[i].Anzahl_Runden = g.Rennen_Runden
			g.Fahrzeug_list[i].Vorsprung = 0
#	g.timer_time = 0
	g.Boot_time = time.time()
	g.time_jump = 0
	g.gefahrene_Zeit=0
	
def clear_vehicle(i):
	global g
	g.Fahrzeug_list[i].Zeit_Runde_Start = timer_time()
	g.Fahrzeug_list[i].Zeit_letzte_Runde = 0.0
	g.Fahrzeug_list[i].Zeit_beste_Runde = 99.99
	g.Fahrzeug_list[i].Anzahl_Runden = 0
	g.Fahrzeug_list[i].Vorsprung = 0


def Buzzer_out(sec):
	GPIO.output(p.Buzzer, True)
	time.sleep(sec)
	GPIO.output(p.Buzzer, False)

def Fanfahre():
	Buzzer_out(0.2)
	time.sleep(0.2)
	Buzzer_out(0.2)
	time.sleep(0.2)
	Buzzer_out(1)
	
def toggle_LED():
	global Flip
	
	if Flip == True:
		LED_R_on(p.LED_R[0])
		LED_R_on(p.LED_R[2])
		LED_R_on(p.LED_R[4])
		LED_R_on(p.LED_R[5])
		LED_R_on(p.LED_R[7])
		LED_R_on(p.LED_R[9])
		LED_off(p.LED_R[1])
		LED_off(p.LED_R[3])
		LED_off(p.LED_R[6])
		LED_off(p.LED_R[8])
		Flip = False
	else:
		LED_off(p.LED_R[0])
		LED_off(p.LED_R[2])
		LED_off(p.LED_R[4])
		LED_off(p.LED_R[5])
		LED_off(p.LED_R[7])
		LED_off(p.LED_R[9])
		LED_R_on(p.LED_R[1])
		LED_R_on(p.LED_R[3])
		LED_R_on(p.LED_R[6])
		LED_R_on(p.LED_R[8])
		Flip = True
	time.sleep(0.0)

def reset_LED():
	for i in range(0,10):
		LED_off(p.LED_R[i])
		