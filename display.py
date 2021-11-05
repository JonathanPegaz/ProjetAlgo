import pygame
from pygame.image import save
import random
from model import screen, screenW, screenH, DISTANCE_PIXEL_DEFAUT

COLOR_INACTIVE = pygame.Color(255,255,255)
COLOR_ACTIVE = pygame.Color(18,242,0)
FONT = pygame.font.Font(None, 32)
input_boxes = []
create_input_boxes = []
display_souris_box = []
info_box = []


class InputBox:

    def __init__(self, inputType, x, y, w, h, text='', textsupp='', boxfield=''):
        self.inputType = inputType
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.textsupp = textsupp
        self.boxfield = boxfield
        self.txt_surface = FONT.render(text + " " + textsupp, True, COLOR_INACTIVE)
        self.active = False
        self.save = False
        self.isChanged = False
        self.rdmImage = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.inputType == 'save':
                    self.save = True
                if self.inputType == 'rdmImage':
                    self.rdmImage = random.randint(1,21)
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if self.inputType == 'input':
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text+self.textsupp, True, self.color)
                    self.isChanged = True
        
    def update(self):
        pass
        # Resize the box if the text is too long.
        # width = max(400, self.txt_surface.get_width()+10)
        # self.rect.x = width
        # self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        self.txt_surface = FONT.render(self.text + " " + self.textsupp, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def display_modification_menu(body, rectimg):
    if(body):
        input_box_name = InputBox('input',screenW-420, rectimg.h + 50, 400, 30, body.name, '', 'name')
        input_box_mass = InputBox('input',screenW-420, rectimg.h + 100, 400, 30, str(body.mass), 'kg', 'mass')
        input_box_distance = InputBox('input',screenW-420, rectimg.h + 150, 400, 30, str(round(body.distance_soleil/DISTANCE_PIXEL_DEFAUT,1)),"million km", 'distance')
        input_box_vitesse = InputBox('input',screenW-420, rectimg.h + 200, 400, 30, str(round(body.initialVelocity.x,0)),"m/s", 'vitesse')
        input_box_save = InputBox('save', screenW-420, rectimg.h + 250, 400, 30, 'save')
        return [input_box_name, input_box_mass, input_box_distance, input_box_vitesse, input_box_save]

def display_create_menu(rectimg):
    create_input_rdm_img = InputBox('rdmImage',10, screenH - rectimg.h - 35, 100, 30, 'random')
    create_input_box_name = InputBox('input',rectimg.w + 20, screenH - 250, 250, 30, 'Damas Planet', 'name', 'name')
    create_input_box_radius = InputBox('input',rectimg.w + 20, screenH - 200, 250, 30, '10500', 'km', 'radius')
    create_input_box_mass = InputBox('input',rectimg.w + 20, screenH - 150, 250, 30, '5.658e+23', 'kg', 'mass')
    create_input_box_vitesse = InputBox('input',rectimg.w + 20, screenH - 100, 250, 30, '25000',"m/s", 'vitesse')
    create_input_box_save = InputBox('save', rectimg.w + 20, screenH - 50, 250, 30, 'right click for create')
    return [create_input_rdm_img, create_input_box_name, create_input_box_radius, create_input_box_mass, create_input_box_vitesse, create_input_box_save]

def display_info(current_distance, current_time):
    info_box_distance = InputBox('info', 10, 10, 1, 30, str(round(current_distance/DISTANCE_PIXEL_DEFAUT,1)), 'million km/pixel (molette souris haut/bas pour le zoom)')
    info_box_time = InputBox('info', 10, 40, 1, 30, str(current_time), '(F1(-)/F2(+) pour ajuster le temps)')
    info_box_reset = InputBox('info', 10, 70, 1, 30, 'Click sur planete: modification menu', '(F5 reset simulation)')
    info_box_name = InputBox('info', 10, 130, 1, 30, '("m" change les nom affichés et la sélection lunes/planètes)')
    return [info_box_distance, info_box_time, info_box_reset, info_box_name]

def display_souris_mass():
    info_box_Souris = InputBox('input',10, 100, 550, 30, '6e+20', 'kg mass Souris (click molette & changez ici)', 'mass')
    return [info_box_Souris]