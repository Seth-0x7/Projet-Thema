#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
import time

# Configuration
DT_PIN = 5      # GPIO5 (Pin 29)
SCK_PIN = 6     # GPIO6 (Pin 31)
REF_UNIT = 1    # À calibrer plus tard

def clean_and_exit():
    print("Nettoyage...")
    GPIO.cleanup()
    print("Bye!")
    exit()

try:
    # Initialisation
    hx = HX711(dout_pin=DT_PIN, pd_sck_pin=SCK_PIN)
    
    # Option 1: Tare seulement (mise à zéro)
    print("Mise à zéro... Ne rien mettre sur le capteur.")
    hx.zero()
    print("Tare effectuée! Valeur de référence:", hx.get_reference_unit())
    
    # Option 2: Calibration avec poids connu
    # hx.set_scale_ratio(REF_UNIT)  # À utiliser après calibration
    
    print("Début des mesures. Ctrl+C pour arrêter.")
    
    while True:
        try:
            # Lecture brute (sans calibration)
            val = hx.get_raw_data_mean()
            
            # Lecture avec calibration (si configurée)
            # weight = hx.get_weight_mean()
            
            print(f"Valeur brute: {val} | Valeur calibrée: {'N/A' if REF_UNIT==1 else round(weight,2)}")
            time.sleep(0.5)
            
        except (KeyboardInterrupt, SystemExit):
            clean_and_exit()
        except Exception as e:
            print("Erreur:", e)
            clean_and_exit()

except Exception as e:
    print("Erreur initiale:", e)
    clean_and_exit()
