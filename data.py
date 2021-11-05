import requests
import math
import random
import pygame
from model import CelestialBody, DISTANCE_PIXEL_DEFAUT, screenH, screenW


list_id_create_planet = ['1', '2', '3', '4', '5', '6',
'7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '20', '21', '22']
params_planets = {'filter[]':'isPlanet,neq,false'}

def createObj(NomObjet, NomClass, params):
    NomObjet = NomClass(*params)
    return NomObjet

def createSourisPlanete(current_distance_pixel, x, y, massSouris):
    value = massSouris.split('e')
    mass = ((float(value[0]))*(10**int(value[1])))
    x -= screenW/2
    y = screenH/2 - y
    img = pygame.image.load('./ressources/souris.png')
    souris = CelestialBody('souris', True, current_distance_pixel, mass,5, 0, 0, x*current_distance_pixel, y*current_distance_pixel, img)
    return souris

def createUserPlanete(create_input_boxes, x, y, create_planete_img, current_distance_pixel):
    velocity = pygame.Vector2(0, 0)
    params = []
    name = ''
    mass = 1.000
    vitesse = 1.000
    radius = 1
    for create_box in create_input_boxes:
        if create_box.boxfield == 'name':
            name = create_box.text
        if create_box.boxfield == 'mass':
            value = create_box.text.split('e')
            mass = ((float(value[0]))*(10**int(value[1])))
        if create_box.boxfield == 'vitesse':
            vitesse = float(create_box.text)
        if create_box.boxfield == 'radius':
            radius = float(create_box.text) * 1000
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
    params = [name, True, current_distance_pixel, mass, radius, velocity.x, velocity.y, x*current_distance_pixel, y*current_distance_pixel, create_planete_img]
    id = random.randint(1,1000000)
    return createObj(id, CelestialBody, params)

def createMoons(moon, planete_speed, planet_distance, central_planet):
    response_moon = requests.get(moon['rel'])
    m = response_moon.json()
    img = pygame.image.load('./ressources/moon.png')
    id = random.randint(1000000,10000000)
    perimetre_revolution =  2 * math.pi * (m["semimajorAxis"])
    temps_revolution = m["sideralOrbit"] * 24 
    vitesse = (perimetre_revolution/temps_revolution)*1000 #metre/h
    vitesse = vitesse / (60*60) #metre/sec
    params = [m["id"], m["isPlanet"], DISTANCE_PIXEL_DEFAUT, m["mass"]["massValue"] * math.pow(10, m["mass"]["massExponent"]), m["meanRadius"]*2*1000, planete_speed + vitesse, 0, 0, (m["semimajorAxis"]+planet_distance)*1000, img, central_planet]
    return createObj(id, CelestialBody, params)

def setUp():
    list_obj = []
    response_sun = requests.get('https://api.le-systeme-solaire.net/rest/bodies/soleil')
    s = response_sun.json()
    img = pygame.image.load('./ressources/'+s["id"]+'.png')
    params=[s["id"], True, DISTANCE_PIXEL_DEFAUT, s["mass"]["massValue"] * math.pow(10, s["mass"]["massExponent"]), s["meanRadius"]*2*1000, 0, 0, 0, 0, img]
    list_obj.append(createObj(s["id"], CelestialBody, params))

    response_planets = requests.get('https://api.le-systeme-solaire.net/rest/bodies/', params=params_planets)
    data_planets = response_planets.json()
    planets = data_planets.get('bodies')
    for p in planets:
        perimetre_revolution =  2 * math.pi * p["semimajorAxis"]
        temps_revolution = p["sideralOrbit"] * 24 
        vitesse = (perimetre_revolution/temps_revolution)*1000 #metre/h
        vitesse = vitesse / (60*60) #metre/sec
        img = pygame.image.load('./ressources/'+p["id"]+'.png')
        params=[p["id"], p["isPlanet"], DISTANCE_PIXEL_DEFAUT, p["mass"]["massValue"] * math.pow(10, p["mass"]["massExponent"]), p["meanRadius"]*2*1000, vitesse, 0, 0, p["semimajorAxis"]*1000, img]
        list_obj.append(createObj(p["id"], CelestialBody, params))
        list_moons = p["moons"]
        if list_moons:
            list_moons = list_moons[0:1]
            for m in list_moons:
                list_obj.append(createMoons(m, vitesse, p["semimajorAxis"], p["id"]))
    
    return list_obj