import time

from threading import Thread

from pad4pi import rpi_gpio

import globals as g
import Port_IO as p
import Tools as t
if g.english == False:
	import Anzeige_de as a
else:
	import Anzeige_en as a


k = Thread()
## Keypad
def Key_init():
	factory = rpi_gpio.KeypadFactory()

	keypad = factory.create_keypad(keypad=p.KEYPAD, row_pins=p.ROW_PINS, col_pins=p.COL_PINS)

	

	  # printKey will be called each time a keypad button is pressed
	keypad.registerKeyPressHandler(printKey)

def printKey(key):       # printKey wir nach Tastenduck gestartet und steuert das Programm
	global g
	global k

	g.Keybuffer = g.Keybuffer + str(key)
	print(key)
	t.Buzzer_out(g.Key_tick)
	if k.is_alive() != True:
		k = Thread(target=Keyaction)     
		k.start()

	
	
def Keyaction():	
	
	if g.Statemachine ==0:
		if len(g.Keybuffer) != 0:
			if g.Keybuffer[0] == "A":   #Training
				g.Statemachine = 10
			if g.Keybuffer[0] == "B":   #Qualifikation
				g.Statemachine = 20
			if g.Keybuffer[0] =="C":    #Rennen
				g.Statemachine = 30
			if g.Keybuffer[0] =="D":    #Einstellungen
				g.Statemachine = 40			
			g.Keybuffer=""
		
	
	if g.Statemachine == 5 or g.Statemachine == 25:			#Stopschirm mit Warten auf Tastendruck
		while True:
			if len(g.Keybuffer) != 0:
				g.Keybuffer =""	
				g.Statemachine = 0
				break
	
	if g.Statemachine == 10:        #Training 
		if g.im_rennen == False:
			g.im_rennen = True

			g.Track_in_use.clear()
			for i in range( 0, g.Anzahl_Spuren):
				g.Track_in_use.append(False)  #all tracks are enabled
			t.init_race()
		if len(g.Keybuffer) != 0:
			i = ord(g.Keybuffer[0])
			if i >= 65 and i <= 68:			#A - D pressed
				t.clear_vehicle(i-65)
			else:	
				g.Statemachine = 0
				g.im_rennen = False
			g.Keybuffer =""
			return
	
	if (g.Statemachine == 20 or g.Statemachine == 30)and g.im_rennen != True:    # rennen oder quali wird vorbereitet
		g.im_rennen = True
		temp = g.Statemachine
#		print("Keyhander "+str(temp))
		t.init_race()
		g.Statemachine = 15  #Startaufstellung
		exit = False
		ignore = False
		while any(g.Sensor_list) == True:
			time.sleep(1)
			print("wait")
			if len(g.Keybuffer) != 0:
				if g.Keybuffer[0] == "*":
					g.Statemachine = 0
					g.im_rennen = False
					g.Keybuffer=""
					exit = True
					break
				if g.Keybuffer[0] =='#':
					ignore = True
					g.Keybuffer=""
					break
				g.Keybuffer =""
		if exit != True:
			g.Track_in_use.clear()
			for i in range( 0, g.Anzahl_Spuren):
				g.Track_in_use.append(g.Sensor_list[i])
			g.Statemachine = 18  # Countdown
			t.Startampel()
			for i in range(0,g.Anzahl_Spuren):
				if g.Track_in_use[i]!= g.Sensor_list[i]:  # prüfen auf Fehlstart
					exit = True
			if exit == True:
				g.im_rennen = False
				g.Statemachine = 25
		if exit != True:	
			g.Statemachine = temp
			t.init_race()
			t.LED_G_on(6)
			t.LED_G_on(14)
			t.Buzzer_out(0.2)
			t.time.sleep(3)
			t.LED_off(6)
			t.LED_off(14)
			
			g.Keybuffer=""
			return

		
	if (g.Statemachine == 20 or g.Statemachine == 30)and g.im_rennen == True:
		temp = g.Statemachine
		while True:
			if len(g.Keybuffer) != 0:
#				if g.Keybuffer[0] =="*":
				if True:    #Konstrukt um obere Kommentarzeile als Option zu halten
					g.Keybuffer = ""
					g.Statemachine = 35
					if confirm() == True:    
						g.im_rennen = False
						g.Statemachine = 0
						break
					else:
						g.Statemachine = temp
						break
	
	if g.Statemachine == 40:
		
		if len(g.Keybuffer) != 0:
			if g.Keybuffer[0] =="*":
				g.Statemachine = 0
			if g.Keybuffer[0] =="A":
				a.update = False
				time.sleep(1)   # Anzeige wird angehalten. Die Zeit stellt sicher, dass keine Zugriffe auf das Display erfolgen
				tempstring=""
				
				a.Set_Cursor_a(0,15)
				g.Keybuffer=""
				tempstring = get_number()
				g.Quali_Zeit=int(tempstring)*600
				a.lcd_a.write_string(tempstring)
				tempstring = get_number()
				g.Quali_Zeit+=int(tempstring)*60
				a.lcd_a.write_string(tempstring)
				a.Reset_cursor_a()
				a.home_a()
				a.update = True
				g.Keybuffer="x"   #notwendig, da get_number den Buffer löscht und die folgende Abfrage indexfehler hervorruft
			
			if g.Keybuffer[0] =="B":
				a.update = False
				time.sleep(1)
				tempstring=""
				a.Set_Cursor_a(1,14)
				g.Keybuffer=""
				tempstring = get_number()
				g.Rennen_Runden=int(tempstring)*100
				a.lcd_a.write_string(tempstring)
				tempstring = get_number()
				g.Rennen_Runden+=int(tempstring)*10
				a.lcd_a.write_string(tempstring)
				tempstring = get_number()
				g.Rennen_Runden+=int(tempstring)
				a.lcd_a.write_string(tempstring)				
				a.Reset_cursor_a()
				a.home_a()
				a.update = True
				g.Keybuffer="x" 
			if g.Keybuffer[0] =="C":
				g.Statemachine = 45
			g.Keybuffer=""
	
	if g.Statemachine == 45:	
		if len(g.Keybuffer) != 0:
			if g.Keybuffer[0] =="*":
				g.Statemachine = 40
			if g.Keybuffer[0] =="#":
				for i in range(0,4):
					g.Fahrzeug_list[i].Vorsprung = 0
			if g.Keybuffer[0] =="A":
				a.update = False
				time.sleep(1)
				tempstring=""
				a.Set_Cursor_a(1,3)
				g.Keybuffer=""
				tempstring = get_number()
				g.Fahrzeug_list[0].Vorsprung = int(tempstring)*10
				a.lcd_a.write_string(tempstring)
				tempstring = get_number()
				g.Fahrzeug_list[0].Vorsprung += int(tempstring)
				a.lcd_a.write_string(tempstring)		
				a.Reset_cursor_a()
				a.home_a()
				a.update = True
				g.Keybuffer="x"  
			if g.Keybuffer[0] =="B":
				a.update = False
				time.sleep(1)
				tempstring=""
				a.Set_Cursor_a(1,14)
				g.Keybuffer=""
				tempstring = get_number()
				g.Fahrzeug_list[1].Vorsprung = int(tempstring)*10
				a.lcd_a.write_string(tempstring)
				tempstring = get_number()
				g.Fahrzeug_list[1].Vorsprung += int(tempstring)
				a.lcd_a.write_string(tempstring)		
				a.Reset_cursor_a()
				a.home_a()
				a.update = True
				g.Keybuffer="x"  
			if g.Keybuffer[0] =="C" and g.Anzahl_Spuren == 4:
				a.update = False
				time.sleep(1)
				tempstring=""
				a.Set_Cursor_b(1,3)
				g.Keybuffer=""
				tempstring = get_number()
				g.Fahrzeug_list[2].Vorsprung = int(tempstring)*10
				a.lcd_b.write_string(tempstring)
				tempstring = get_number()
				g.Fahrzeug_list[2].Vorsprung += int(tempstring)
				a.lcd_b.write_string(tempstring)		
				a.Reset_cursor_b()
				a.home_b()
				a.update = True
				g.Keybuffer="x"  
			if g.Keybuffer[0] =="D" and g.Anzahl_Spuren == 4:
				a.update = False
				time.sleep(1)
				tempstring=""
				a.Set_Cursor_b(1,14)
				g.Keybuffer=""
				tempstring = get_number()
				g.Fahrzeug_list[3].Vorsprung = int(tempstring)*10
				a.lcd_b.write_string(tempstring)
				tempstring = get_number()
				g.Fahrzeug_list[3].Vorsprung += int(tempstring)
				a.lcd_b.write_string(tempstring)		
				a.Reset_cursor_b()
				a.home_b()
				a.update = True
			g.Keybuffer=""
			
		
def confirm():
	global g
	confirm = False
	decission = False
	while decission != True:
		if len(g.Keybuffer) != 0:
			if g.Keybuffer[0] =="*": # Abbruch Rennen/Quali und zurück ins Hauptmenu
				decission = True
				confirm = False
			if g.Keybuffer[0] == '#':
				decission = True
				confirm = True
			g.Keybuffer =""
		time.sleep(0.5)
	return confirm
	
def get_number():
	global g
	number = ""
	keyfound = False	
	while keyfound != True:
		if len(g.Keybuffer) != 0:
			if g.Keybuffer[0] != '*' and g.Keybuffer[0] != '#' and g.Keybuffer[0] != 'A' and g.Keybuffer[0] != 'B' and g.Keybuffer[0] != 'C' and g.Keybuffer[0] != 'D':
				keyfound = True
				number = g.Keybuffer[0]
			g.Keybuffer =""
		time.sleep(0.5)
	return number