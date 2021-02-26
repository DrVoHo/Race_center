Anzahl_Spuren = 0  #number off tracks - depends on number of Sensors (Port_IO: SEN array)

english = False

Boot_time = 0.0

Debounce = 50

Statemachine = 0

Startzeit = 0
Gesamtzeit = 0

gefahrene_Zeit=0

timer_time = 0.0

Quali_Zeit = 600    #time for Quali in seconds

Rennen_Runden = 20  #laps in race

Fahrzeug_list =[]

Sensor_list = []

Track_in_use = []

Sensor = True  #Signal high ->  kein Auto unter dem Sensor.

im_rennen = False


Keybuffer = ""
Key_tick = 0.01   #0 for disabling keytick

LED_W_dim = 95
LED_G_dim = 100
LED_R_dim = 100





class Fahrzeug:
	def __init__(self, Start, lRunde,bRunde,Runden,hc):  
		self.Zeit_Runde_Start = Start
		self.Zeit_letzte_Runde = lRunde
		self.Zeit_beste_Runde = bRunde
		self.Anzahl_Runden = Runden
		self.Vorsprung = hc



def global_init():
	global Fahrzeug_list
	global Sensor_list
	global Track_in_use
	global Message_a
	global Message_b
	global Fahrzeug
	for i in range(0,Anzahl_Spuren):		
		Sensor_list.append(Sensor)  #Sensoren auf Anzahl der Spuren begrenzt wegen Erkennung Startaufstellung und Fehlstart
		Track_in_use.append(False)
		Fahrzeug_list.append(Fahrzeug(0.0,0.0,99.99,0,0))


		



