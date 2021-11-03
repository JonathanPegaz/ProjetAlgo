import pygame
from data import list_id_create_planet, createUserPlanete, setUp, createSourisPlanete
from model import screen, screenW, screenH, current_distance_pixel
from display import (display_create_menu, display_modification_menu,
                    input_boxes, create_input_boxes,COLOR_ACTIVE,
                    COLOR_INACTIVE, info_box, display_info, display_souris_mass,
                    display_souris_box)

pygame.init()

list_celestial_bodies = []


screen.fill((0,0,0))


play = True
clock = pygame.time.Clock()
mouse = (0,0)
time_elapsed = 1
actual_selected_bodie = None
new_selected_bodie = None
create_planete_img = pygame.image.load('./ressources/'+list_id_create_planet[0]+'.png')
inCreation = False
sourisDisplay = False
souris = None
isMousePlanete = False
massSouris = '6e+25'


while play:
    event_list = pygame.event.get()
    for event in event_list:
        if isMousePlanete == True:
            pygame.mouse.set_pos(souris.position2D.x, souris.position2D.y)
        if(display_souris_box):
            for box in display_souris_box:
                box.handle_event(event)
        if(input_boxes):
            for box in input_boxes:
                box.handle_event(event)
        if(create_input_boxes):
            for create_box in create_input_boxes:
                create_box.handle_event(event)
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            mouse = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bodies in list_celestial_bodies:
                    if (bodies.position2D.x-bodies.radius2D)<x and (bodies.position2D.x+bodies.radius2D)>x and (bodies.position2D.y-bodies.radius2D)<y and (bodies.position2D.y+bodies.radius2D)>y:
                        new_selected_bodie=bodies
            if event.button == 2:
                if isMousePlanete == False:
                    if souris == None:
                        souris = createSourisPlanete(current_distance_pixel, x, y, massSouris)
                        list_celestial_bodies.append(souris)
                        isMousePlanete = True
            if event.button == 3:
                x,y = event.pos
                if(create_input_boxes):
                    list_celestial_bodies.append(createUserPlanete(create_input_boxes, x, y, create_planete_img, current_distance_pixel))
            if event.button == 4:
                for bodies in list_celestial_bodies:
                    bodies.zoomUp()
            if event.button == 5:
                for bodies in list_celestial_bodies:
                    bodies.zoomDown()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                if isMousePlanete == True:
                    list_celestial_bodies.remove(souris)
                    souris = None
                    isMousePlanete = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                for bodies in list_celestial_bodies:
                    bodies.timeFactor(-1)
            if event.key == pygame.K_F2:
                for bodies in list_celestial_bodies:
                    bodies.timeFactor(1)
            if event.key == pygame.K_F5:
                list_celestial_bodies = []
                inCreation = False
                sourisDisplay = False
                actual_selected_bodie = None
                new_selected_bodie = None

    screen.fill((0,0,0))
    if(list_celestial_bodies == []):
        list_celestial_bodies = setUp()
    if(list_celestial_bodies):
     info_obj = list_celestial_bodies[0]
    current_distance_pixel = info_obj.distance_pixel
    info_box = display_info(current_distance_pixel, info_obj.timeDescription)
    if(info_box):
        for box in info_box:
            box.update()
            box.draw(screen)

    if(sourisDisplay == False):
        display_souris_box = display_souris_mass()
        sourisDisplay = True
    if(display_souris_box):
        for box in display_souris_box:
            box.update()
            box.draw(screen)
            if box.text != massSouris:
                massSouris = box.text

    # gestion planetes
    for bodies in list_celestial_bodies:
        bodies.updateVelocity(list_celestial_bodies)
    for bodies in list_celestial_bodies:
        bodies.updatePosition()
        if(bodies.radius2D >=1):
            screen.blit(bodies.namesurface,(bodies.position2D.x, bodies.position2D.y))
            rect = bodies.getImage().get_rect()
            rect.center = bodies.position2D.x, bodies.position2D.y
            screen.blit(bodies.getImage(), rect)

    #gestion selection planete et affichage caractéristiques
    if(new_selected_bodie):
        rectimg = new_selected_bodie.img.get_rect()
        screen.blit(new_selected_bodie.img, (screenW - rectimg.w, 0))
    if(actual_selected_bodie!=new_selected_bodie):
        actual_selected_bodie = new_selected_bodie
        input_boxes = display_modification_menu(new_selected_bodie, rectimg)
    #gestion actualisation box planetes selectionné et sauvegarde changement
    if(input_boxes):
        for box in input_boxes:
            box.update()
            box.draw(screen)
            if box.save == True:
                actual_selected_bodie.modif_body(input_boxes)
                box.save = False
                for box in input_boxes:
                    box.color = COLOR_INACTIVE
                    box.isChanged = False


    rect_img_create = create_planete_img.get_rect()
    screen.blit(create_planete_img, (10, screenH - rect_img_create.h))
    if(inCreation == False):
        create_input_boxes = display_create_menu(rect_img_create)
        inCreation = True

    if(create_input_boxes):
        for create_box in create_input_boxes:
            create_box.update()
            create_box.draw(screen)
            if create_box.rdmImage > 0:
                create_planete_img = pygame.image.load('./ressources/'+list_id_create_planet[create_box.rdmImage]+'.png')

    time_elapsed += clock.tick(60)
    pygame.display.flip()