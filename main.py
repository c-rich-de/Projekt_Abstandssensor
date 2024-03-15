from machine import ADC      #Initialisieren des ADC
from time import sleep       #Initialisieren Sleep-Befehls aus dem 'time' Moduls

#I2C betriebenenes SH1106 OLED-Display 
from machine import I2C, ADC
from sh1106 import SH1106_I2C
import framebuf

WIDTH  = 128                                           #Breite des OLED-Displays
HEIGHT = 64                                            #Höhe des OLED-Displays

i2c = I2C(0)             #I2C mit I2C0 defaults, SCL=Pin(GP5), SDA=Pin(GP4), freq=400000

print("I2C Address      : "+hex(i2c.scan()[0]).upper()) #Display device address
print("I2C Configuration: "+str(i2c))                   #Display I2C config

oled = SH1106_I2C(WIDTH, HEIGHT, i2c)                  #Initialisierung des OLED-Displays
oled.rotate(True)                                      #Drehen des Bildes um 180 Grad

#Sensor-Anschluss
from machine import Pin, PWM                #Initialisierung der PWM-Funktionseinheit 
pwm = PWM(Pin(19))                          #und des GPIO-Pins
pwm.freq(13)                                #Einstellen der Frequenz für die PWM
pwm.duty_u16(65535)                         #Einstellen vom Tastgrad (Duty Cycle)
pot = ADC(Pin(26))                          #Festlegung des Pins für den ADC

#log-file erstellen
file = open("data.csv","w")

#Definition von max und min
max_abstand = 0                             #umgekehrte Proportionalität
min_abstand = 65535

#Durchlauf mit Anzeige von Werten
while True:
  #ADC
  pot_value = pot.read_u16()
  #Berechnung der Anzeigewerte
  pot_spannung = (3.3 * pot_value)/65535
  abstand = (pot_spannung - 5.61)/(-1.05)
  max_abstand = max(abstand, max_abstand)
  min_abstand = min(abstand, min_abstand)
  diff = max_abstand - min_abstand
  #Ausgabe in der Shell zur Kontrolle
  print(pot_value)
  print(pot_spannung)
  print(abstand)
  #OLED-Display (l/r, o/u)
  #Abstandsanzeige
  oled.text("Abstand:",5,5)
  oled.text(str(abstand)[:5],5,15)
  oled.text("mm",55,15)
  #Füller
  oled.text("-------------------",0,23)
  #Max/Min Anzeige
  oled.text("max:   min:",5,30)
  oled.text(str(max_abstand)[:5],5,40)
  oled.text(str(min_abstand)[:5],60,40)
  oled.text("mm",110,40)
  #Differenzanzeige
  oled.text("Diff.:",5,55)
  oled.text(str(diff)[:5],60,55)
  oled.text("mm",110,55)
  #Ausgabe des Displays
  oled.show()
  sleep(0.08)    #für weniger häufige Aktualisierung der Messwerte (auf pwm.freq abgestimmt!)
  oled.fill(0)   #reset des OLED-Displays auf schwarz
  #Füllen des log-files
  file.write("Wert: " + str(pot_value) + "| Spannung (V): " + str(pot_spannung) + 
  "| Abstand (mm): " + str(abstand) + "\n")
  file.flush()
