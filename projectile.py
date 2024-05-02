import pygame
from ext import *
import os
import math

from extras import*

projectile_list = pygame.sprite.Group()

class Acid_spell(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image_orig, self.rect = load_image("acid.png", -1)

        #flip acid to the left or right
        
        self.image_flipped = pygame.transform.flip(self.image_orig, True, False)
        self.image = self.image_flipped if dest_x < start_x else self.image_orig

        self.image = self.image_orig
        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y
 
        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y
 
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);
 
        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
    def update(self):
        """ Move the bullet. """
 

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
 
        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

    def rotate_spell(self, image, angle):
        image_rect = image.get_rect()
        center = image_rect.center


        
        rotated_image = pygame.transform.rotate(image, angle)

        rotated_rect = rotated_image.get_rect(center=center)

        return rotated_image, rotated_rect
