import time

import globals as g
import Port_IO as p
import Tools as t
from RPLCD.i2c import CharLCD

lcd_a = CharLCD('PCF8574', p.LCD_A)
if g.Anzahl_Spuren == 4:
	lcd_b = CharLCD('PCF8574', p.LCD_B)

update = True  #update der Anzeige kann unterbunden werden (Zahleneingabe)

Message = []  #index 0-3: LCD A; index 4-7 LCD B


def Anzeige():
	global g
	global Message
	for i in range(0,8):
		Message.append("")   #index 0-3: LCD A; index 4-7 LCD B
	

	while True:
		
		time.sleep(0.1)
		print(g.Statemachine)
		if g.Statemachine == 0:  #Startschirm
			Startschirm()
		if g.Statemachine == 5:  #Ergebnis
			Ergebnis()
		if g.Statemachine == 10: #Training
			Training()
		if g.Statemachine == 15: #Vorbereitung Start
			Startaufstellung()
		if g.Statemachine == 18: #Startampel
			CountDown()
		if g.Statemachine == 20:  #Qualifikation
			if Quali() == False:
				g.Statemachine = 5
		if g.Statemachine == 25:  #Fehlstart
			Fehlstart()
		if g.Statemachine == 30:  #Rennen
			if Rennen()== False:
				g.Statemachine = 5
		if g.Statemachine == 35:  #Rennen abbrechen?
			Confirm()
		if g.Statemachine == 40:  #Einstellungen
			Einstellungen()
		if g.Statemachine == 45:  #Vorsprung
			Vorsprung()
		if update == True:
			lcd_a.home()
			for j in range (0,4):
				lcd_a.write_string(Message[j])
			if g.Anzahl_Spuren == 4:
				lcd_b.home()	
				for j in range (0,4):
					lcd_b.write_string(Message[j+4])



def Startschirm():  #Statemachin = 0
	global g
	global Message
	
	Message[0] ="A: Training         "
	Message[1] ="B: Qualifikation    "
	Message[2] ="C: Rennen           "
	Message[3] ="D: Einstellungen    "
	for i in range(0,4):
		Message[i+4] = "                    "
			
def Training(): #Statemachine = 10
	global g
	global Message
	for i in range(0,int(g.Anzahl_Spuren/2)): #max 2 display
		Message[4*i] ="  %0.3u  Runden    %0.3u" %(g.Fahrzeug_list[2*i].Anzahl_Runden, g.Fahrzeug_list[2*i+1].Anzahl_Runden)
		min,sec = divmod(g.timer_time,60)
		if g.timer_time > 6000:
			min = 99
			sec = 59
		Message[4*i+1] ="%0.2u:%0.2u   Zeit   %0.2u:%0.2u"%(min,sec,min,sec)
	
	Rundenzeit()

	
def Quali():  #Statemachine = 20
	global g
	temp=["","","","","","","",""]
	global Message

	if g.Quali_Zeit >= g.timer_time:

		min,sec = divmod(g.Quali_Zeit - g.timer_time,60)

		for i in range(0,int(g.Anzahl_Spuren/2)): #max 2 display
			for j in range(0,2):
				if g.Track_in_use[2*i+j] == False:  #Track in use - inverted logic
					temp[4*i+2*j] = "%0.3u"%(g.Fahrzeug_list[2*i+j].Anzahl_Runden+g.Fahrzeug_list[2*i+j].Vorsprung)
					temp[4*i+2*j+1] ="%0.2u:%0.2u"%(min,sec)
				else:
					temp[4*i+2*j] = "   "
					temp[4*i+2*j+1] ="     "

			Message[4*i] ="  " + temp[4*i] +"  Runden    " + temp[4*i+2]  
			Message[4*i+1] =temp[4*i+1] +"  Zeit    " + temp[4*i+3] 

		
		Rundenzeit()
	else: 
		g.im_rennen = False
		g.gefahrene_Zeit = g.timer_time
		t.Fanfahre()
	return(g.im_rennen)

def Startaufstellung():	
	global g
		
	Message[0] ="                    "
	Message[1] =" Autos in Startpos. " 
	Message[2] =" '*' Abbrechen      "
	Message[3] =" '#' Weiter         "
	for i in range(0,4):
		Message[i+4] = "                    "

def CountDown():
	Message[0] ="      XXXXXXX       "
	Message[1] ="       XX XX        " 
	Message[2] ="        XXX         "
	Message[3] ="         X          "
	
	Message[4] ="      XXXXXXX       "
	Message[5] ="       XX XX        " 
	Message[6] ="        XXX         "
	Message[7] ="         X          "

def Rennen(): #Statemachine = 30
	global g
	global Message
	temp=["","","","","","","",""]
	

	if g.im_rennen == True:
		min,sec = divmod(g.timer_time,60)
		if g.timer_time > 6000:
			min = 99
			sec = 59
		for i in range(0,int(g.Anzahl_Spuren/2)): #max 2 display
			for j in range(0,2):
				if g.Track_in_use[2*i+j] == False:  #Track in use - inverted logic
					temp[4*i+2*j] = "%0.3u"%(g.Rennen_Runden-g.Fahrzeug_list[2*i+j].Anzahl_Runden+g.Fahrzeug_list[2*i+j].Vorsprung)
					temp[4*i+2*j+1] ="%0.2u:%0.2u"%(min,sec)
				else:
					temp[4*i+2*j] = "   "
					temp[4*i+2*j+1] ="     "

			Message[4*i] ="  " + temp[4*i] +"  Runden    " + temp[4*i+2]  
			Message[4*i+1] =temp[4*i+1] +"  Zeit    " + temp[4*i+3] 

		
		Rundenzeit()
	return(g.im_rennen)

def Rundenzeit():
	global g
	global Message
	temp=["","","","","","","",""]
	
	for i in range(0,int(g.Anzahl_Spuren/2)): #max 2 display
		for j in range(0,2):
			if g.Track_in_use[2*i+j] == False:  #Track in use - inverted logic
				temp[4*i+2*j] = "%05.2f"%(g.Fahrzeug_list[2*i+j].Zeit_letzte_Runde)
				if g.Fahrzeug_list[2*i+j].Zeit_letzte_Runde >99.99:
					temp[4*i+2*j]="99.99"
				temp[4*i+2*j+1] ="%05.2f"%(g.Fahrzeug_list[2*i+j].Zeit_beste_Runde)
				if g.Fahrzeug_list[2*i+j].Zeit_beste_Runde >99.99:
					temp[4*i+2*j+1]="99.99"
				if g.Fahrzeug_list[2*i+j].Zeit_beste_Runde == 99.99:
					temp[4*i+2*j+1]	="--:--"
			else:
				temp[4*i+2*j] = "     "
				temp[4*i+2*j+1] ="     "

		Message[4*i+2] =temp[4*i] +"  Letzte  " + temp[4*i+2]  
		Message[4*i+1+2] =temp[4*i+1] +"  Beste   " + temp[4*i+3] 
	


def Ergebnis():
	temp=["","","","","","","",""]
	min,sec = divmod(g.gefahrene_Zeit,60)
	if g.gefahrene_Zeit > 6000:
		min = 99
		sec = 59
	for i in range(0,int(g.Anzahl_Spuren/2)): #max 2 display
		for j in range(0,2):
			if g.Track_in_use[2*i+j] == False:  #Track in use - inverted logic
				temp[4*i+2*j] = "%0.3u"%(g.Fahrzeug_list[2*i+j].Anzahl_Runden+g.Fahrzeug_list[2*i+j].Vorsprung)
				temp[4*i+2*j+1] ="%0.2u:%0.2u"%(min,sec)
			else:
				temp[4*i+2*j] = "   "
				temp[4*i+2*j+1] ="     "

		Message[4*i] ="  " + temp[4*i] +"  Runden    " + temp[4*i+2]  
		Message[4*i+1] =temp[4*i+1] +"  Zeit    " + temp[4*i+3] 

	
	Rundenzeit()

def Fehlstart():
	global g
			
	Message[0] ="                    "
	Message[1] ="   Fehlstart !      " 
	Message[2] ="                    "
	Message[3] ="  Taste druecken    "
	for i in range(0,4):
		Message[i+4] = "                    "

def Confirm():
	Message[0] ="                    "
	Message[1] =" Rennen abbrechen?  " 
	Message[2] ="                    "
	Message[3] ="  '#' Ja   '*' Nein "
	for i in range(0,4):
		Message[i+4] = "                    "

def Einstellungen():
	global g
	
	Message[0] ="A: Zeit Quali  %0.2umin"%(int(g.Quali_Zeit/60))
	Message[1] ="B: Runden     %0.3u   "%(g.Rennen_Runden)
	Message[2] ="C: Vorsprung        "
	Message[3] ="   '*' Zurueck      "
	for i in range(0,4):
		Message[i+4] = "                    "

def Vorsprung():
	global g
	Message[0] ="                    "
	Message[1] =" A:%0.2u       B:%0.2u     "%(g.Fahrzeug_list[0].Vorsprung, g.Fahrzeug_list[1].Vorsprung)
	Message[2] =" '#'  Loeschen      "
	Message[3] =" '*'  Zurueck       "
	
	Message[4] ="                    "
	Message[5] =" C:%0.2u       D:%0.2u    " %(g.Fahrzeug_list[2].Vorsprung, g.Fahrzeug_list[3].Vorsprung)
	Message[6] ="                    "
	Message[7] ="                    " 
	
##low level funktionen für die Zahleneingabe

def Set_Cursor_a(Zeile,Spalte):
	lcd_a.cursor_mode = 'blink'
	lcd_a.cursor_pos = (Zeile, Spalte)

def write_String_a(String):
	lcd_a.write_string(String)
	
def Reset_cursor_a():
	lcd_a.cursor_mode = 'hide'
	
def home_a():
	lcd_a.home()

def Set_Cursor_b(Zeile,Spalte):
	lcd_b.cursor_mode = 'blink'
	lcd_b.cursor_pos = (Zeile, Spalte)

def write_String_b(String):
	lcd_b.write_string(String)
	
def Reset_cursor_b():
	lcd_b.cursor_mode = 'hide'
	
def home_b():
	lcd_b.home()