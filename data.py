import requests
import math
import random
import pygame
from model import CelestialBody, DISTANCE_PIXEL_DEFAUT, screenH, screenW

list_celestial_bodies = []
list_id_create_planet = ['1', '2', '3', '4', '5', '6',
'7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '20', '21', '22']
params_planets = {'filter[]':'isPlanet,neq,false'}

def createObj(NomObjet, NomClass, params):
    NomObjet = NomClass(*params)
    list_celestial_bodies.append(NomObjet)

def createUserPlanete(create_input_boxes, x, y, create_planete_img):
    print(x,y)
    velocity = pygame.Vector2(0, 0)
    params = []
    name = ''
    mass = 1.000
    vitesse = 1.000
    for create_box in create_input_boxes:
        if create_box.boxfield == 'name':
            name = create_box.text
        if create_box.boxfield == 'mass':
            value = create_box.text.split('e')
            mass = ((float(value[0]))*(10**int(value[1])))
        if create_box.boxfield == 'vitesse':
            vitesse = float(create_box.text)
    if x > screenW/2 and y < screenH/2: #++
        velocity.x = vitesse
    elif x > screenW/2 and y > screenH/2: #+-
        velocity.x = -vitesse
    elif x < screenW/2 and y > screenH/2: #--
        velocity.x = vitesse
    elif x < screenW/2 and y < screenH/2: #-+
        velocity.x = vitesse
    x -= screenW/2
    y = screenH/2 - y
    print(velocity.x, velocity.y)
    params = [name, mass, 5, velocity.x, velocity.y, x*DISTANCE_PIXEL_DEFAUT, y*DISTANCE_PIXEL_DEFAUT, create_planete_img]
    id = random.randint(1,1000000)
    createObj(id, CelestialBody, params)


response_sun = requests.get('https://api.le-systeme-solaire.net/rest/bodies/soleil')
s = response_sun.json()
img = pygame.image.load('ressources/'+s["id"]+'.png')
params=[s["id"], s["mass"]["massValue"] * math.pow(10, s["mass"]["massExponent"]), s["meanRadius"]*2*1000, 0, 0, 0, 0, img]
createObj(s["id"], CelestialBody, params)

response_planets = requests.get('https://api.le-systeme-solaire.net/rest/bodies/', params=params_planets)
data_planets = response_planets.json()
planets = data_planets.get('bodies')
for p in planets:
    perimetre_revolution =  2 * math.pi * p["semimajorAxis"]
    temps_revolution = p["sideralOrbit"] * 24 
    vitesse = (perimetre_revolution/temps_revolution)*1000 #metre/h
    vitesse = vitesse / (60*60) #metre/sec
    img = pygame.image.load('ressources/'+p["id"]+'.png')
    params=[p["id"], p["mass"]["massValue"] * math.pow(10, p["mass"]["massExponent"]), p["meanRadius"]*2*1000, vitesse, 0, 0, p["semimajorAxis"]*1000, img]
    createObj(p["id"], CelestialBody, params)


