import pygame
import math
screenW, screenH = 1280, 720
screen = pygame.display.set_mode((screenW, screenH))
GRAVITATIONAL_CONSTANT = 6.67408e-11
DISTANCE_PIXEL_DEFAUT = 1000000000 #m
current_distance_pixel = DISTANCE_PIXEL_DEFAUT
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)

class CelestialBody:
    def __init__(self, id, isPlanet, dp, mass, radius, ivx, ivy, posx, posy, img):
        self.name = id
        self.isPlanet = isPlanet
        self.distance_pixel = dp
        self.mass = mass
        self.radius = radius
        self.radius2D = 5#radius/self.distance_pixel
        self.initialVelocity = pygame.Vector2(ivx, ivy)
        self.currentVelocity = pygame.Vector2(ivx, ivy)
        self.position2D =  pygame.Vector2(screenW/2 + posx/self.distance_pixel, screenH/2 - posy/self.distance_pixel)
        self.namesurface = myfont.render(self.name, False, (255, 255, 255))
        self.position = pygame.Vector2(posx, posy)
        self.img = img
        self.distance_soleil = posy
        self.currentTimeFactor = 1
        self.timeSpeed = 1
        self.timeDescription = '1 mois/seconde'
        self.moon2Doffset = 5 #pixel

    def updateVelocity(self, allBodies):
        """Newton's law of universal gravitation : F = G*((m1*m2)/r)"""
        for otherBodies in allBodies:
            if(otherBodies!=self):
                sqrDst = (otherBodies.position - self.position).magnitude()
                forceDir = (otherBodies.position - self.position).normalize()
                force = forceDir * GRAVITATIONAL_CONSTANT * (self.mass * otherBodies.mass / sqrDst**2)
                acceleration = force / self.mass
                self.currentVelocity += acceleration * self.timeSpeed

    def updatePosition(self):
        self.position += self.currentVelocity * self.timeSpeed
        if self.isPlanet == False:
            self.position2D = pygame.Vector2(screenW/2 + self.position.x/self.distance_pixel, screenH/2 - self.position.y/self.distance_pixel)
        else:
            self.position2D = pygame.Vector2(screenW/2 + self.position.x/self.distance_pixel, screenH/2 - self.position.y/self.distance_pixel)

    def zoomUp(self):
        self.distance_pixel *= 1.1
        # self.radius2D = self.radius/self.distance_pixel

    def zoomDown(self):
        self.distance_pixel /= 1.1
        # self.radius2D = self.radius/self.distance_pixel

    def timeFactor(self, value):
        if self.currentTimeFactor + value > 0 and self.currentTimeFactor + value < 8:
            self.currentTimeFactor += value
            if self.currentTimeFactor == 1:
                self.timeSpeed = 1 #1s
                self.timeDescription = '1 seconde/seconde'
            elif self.currentTimeFactor == 2:
                self.timeSpeed = 60 #1m
                self.timeDescription = '1 minute/seconde'
            elif self.currentTimeFactor == 3:
                self.timeSpeed = 3600 #1 jour
                self.timeDescription = '1 jour/seconde'
            elif self.currentTimeFactor == 4:
                self.timeSpeed = 86400 #1 mois
                self.timeDescription = '1 mois/seconde'
            elif self.currentTimeFactor == 5:
                self.timeSpeed = 1036800 # 1 années
                self.timeDescription = '1 année/seconde'
            elif self.currentTimeFactor == 6:
                # attention voir commentaire updateVelocity
                self.timeSpeed = 10368000 # 10 années
                self.timeDescription = '10 années/seconde'
            elif self.currentTimeFactor == 7:
                # attention voir commentaire updateVelocity
                self.timeSpeed = 103680000 # 100 années
                self.timeDescription = '100 années/seconde'

    def getImage(self):
        if self.isPlanet:
            return pygame.transform.scale(self.img, (10,10))
        else:
            return pygame.transform.scale(self.img, (2,2))

    def modif_body(self, input_boxes):
        for box in input_boxes:
            if box.boxfield == 'name' and box.isChanged == True:
                self.name = box.text
                self.namesurface = myfont.render(self.name, False, (255, 255, 255))
            if box.boxfield == 'mass' and box.isChanged == True:
                mass = box.text.split('e')
                ret_mass =((float(mass[0]))*(10**int(mass[1])))
                self.mass = ret_mass
            if box.boxfield == 'vitesse' and box.isChanged == True:
                self.initialVelocity = pygame.Vector2(float(box.text), 0)
                if self.currentVelocity.x > 0 :
                    self.currentVelocity.x = self.initialVelocity.x
                else:
                    self.currentVelocity.x = -self.initialVelocity.x
            if box.boxfield == 'distance' and box.isChanged == True:
                self.distance_soleil = float(box.text)*DISTANCE_PIXEL_DEFAUT
                self.position.y = float(box.text)*DISTANCE_PIXEL_DEFAUT
                self.position.x = 0
                self.currentVelocity = self.initialVelocity
     
            
            