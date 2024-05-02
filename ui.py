import pygame, random, os
from pygame.locals import *
from ext import *
font = pygame.font.Font("assets/Achafexp.ttf", 30)


class UI():
    def __init__(self):
        self




    def some_ui(self, player):
        coord = font.render(f"{player.rect.centerx}, {player.rect.centery}", True, 'red')
        coords = font.render(f"{player.weapon.rect.centerx}, {player.weapon.rect.centery}", True, 'red')
        screen.blit(coord, (0, 0))
        screen.blit(coords, (0, 50))
        mag = font.render(f"{player.mag}/6", True, 'red')
        screen.blit(mag, (0, 670))
        health = font.render(f"{player.health}", True, 'red')
        screen.blit(health, (0, 620))



