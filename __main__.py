import pygame, random, os
from pygame.locals import *
from character import *
from ext import *
from button import *
from ui import *
from enemies import*
from projectile import*
from extras import*

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


pygame.init()


pygame.display.set_caption("Creating Sprite")

menu = 0


def make_menu():
    txt = title_font.render('Crawling in my Skin', True, 'red')
    screen.blit(txt, (450, 0))
    start = Button('Start', (455, 100))
    start.draw()
    if start.check_clicked():
        start_game()
        global menu
        menu += 1

def start_game():
    screen.fill(SURFACE_COLOR)

    global playerCar
    playerCar = Character(200, 300)
    all_sprites_list.add(playerCar)

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    global ui
    ui = UI()

    cult = Cultist(500, 400)
    enemies_list.add(cult)
    



 
run = True
clock = pygame.time.Clock()

while run:
    screen.fill(SURFACE_COLOR)
    
    if menu == 0:
        make_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    

    if menu == 1:
        ui.some_ui(playerCar)

        all_sprites_list.update()
        all_sprites_list.draw(screen)

        weapon_sprite.update()
        weapon_sprite.draw(screen)

        enemies_list.update(playerCar.rect, bullet_list)
        enemies_list.draw(screen)

        projectile_list.update()
        projectile_list.draw(screen)

        bullet_list.update()
        bullet_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)






pygame.quit()
