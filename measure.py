#!/usr/bin/env python3
import RPi.GPIO as GPIO  # importer GPIO
from hx711 import HX711  # importer la classe HX711

try:
    GPIO.setmode(GPIO.BCM)  # configurer le mode des broches GPIO en numérotation BCM
    # Créer un objet hx qui représente votre puce HX711 réelle
    # Les paramètres d'entrée requis sont seulement 'dout_pin' et 'pd_sck_pin'
    hx = HX711(dout_pin=20, pd_sck_pin=21)
    # mesurer la tare et sauvegarder la valeur comme offset pour le canal actuel
    # et le gain sélectionné. Cela signifie canal A et gain 128
    err = hx.zero()
    # vérifier si c'est réussi
    if err:
        raise ValueError('La tare a échoué.')

    reading = hx.get_raw_data_mean()
    if reading:  # toujours vérifier si vous obtenez une valeur correcte ou seulement False
        # maintenant la valeur est proche de 0
        print('Données soustraites par offset mais pas encore converties en unités :',
              reading)
    else:
        print('données invalides', reading)

    # Afin de calculer le ratio de conversion vers des unités, dans mon cas je veux des grammes,
    # vous devez avoir un poids connu.
    input('Placez un poids connu sur la balance puis appuyez sur Entrée')
    reading = hx.get_data_mean()
    if reading:
        print('Valeur moyenne du HX711 soustraite par offset :', reading)
        known_weight_grams = input(
            'Entrez le nombre de grammes que cela représente et appuyez sur Entrée : ')
        try:
            value = float(known_weight_grams)
            print(value, 'grammes')
        except ValueError:
            print('Attendu un entier ou un float et j\'ai reçu :',
                  known_weight_grams)

        # configurer le ratio d'échelle pour un canal et gain particulier qui est
        # utilisé pour calculer la conversion en unités. L'argument requis est seulement
        # le ratio d'échelle. Sans arguments 'channel' et 'gain_A', cela configure
        # le ratio pour le canal et gain actuels.
        ratio = reading / value  # calculer le ratio pour le canal A et gain 128
        hx.set_scale_ratio(ratio)  # configurer le ratio pour le canal actuel
        print('Votre ratio est', ratio)
    else:
        raise ValueError('Impossible de calculer la valeur moyenne. Essayez le mode debug. Variable reading :', reading)

    # Lire les données plusieurs fois et retourner la valeur moyenne
    # soustraite par offset et convertie par le ratio d'échelle vers
    # les unités désirées. Dans mon cas en grammes.
    input('Appuyez sur Entrée pour afficher la lecture')
    print('Le poids actuel sur la balance en grammes est : ', reading)

except (KeyboardInterrupt, SystemExit):
    print('Au revoir :)')

finally:
    GPIO.cleanup()
