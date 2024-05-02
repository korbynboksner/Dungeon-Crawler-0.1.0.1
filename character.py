# Object class
import pygame
from ext import *
import os
import math
from projectile import*
from extras import*


pygame.init()


all_sprites_list = pygame.sprite.Group()
weapon_sprite = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()



shot_sound = load_sound("shot.mp3")
reload_sound = load_sound("reload.mp3")
dry_fire_sound = load_sound("dry.mp3")
shot_sound.set_volume(0.3)  # Set volume to 30%
reload_sound.set_volume(0.8)  # Set volume to 80%
dry_fire_sound.set_volume(1.6)  # Set volume to 160%



def rotate_on_pivot(image, angle):
    
    surf = pygame.transform.rotate(image, angle)
    return surf

class Character(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
 
        self.walk_left_frames = [load_image(f"walk_left_{i}.png", -1)[0] for i in range(1, 4)]
        self.walk_right_frames = [load_image(f"walk_right_{i}.png", -1)[0] for i in range(1, 4)]
        self.image = self.walk_right_frames[0]
        self.rect = self.image.get_rect()
        self.speed = 5
        self.mag = 6
        self.shoot_cooldown = 10
        self.rect.topleft = 32, 32
        self.reload_timer = 0
        self.reload = False
        self.rect.x = position_x
        self.rect.y = position_y
        self.weapon = Player_Weapon()
        self.orbit_angle = 0 
        self.mouse_button_pressed = False
        self.move_x = 0
        self.move_y = 0
        self.health = 6
        
        weapon_sprite.add(self.weapon)

    def input_or_movement(self):


        keys = pygame.key.get_pressed()
        left= keys[pygame.K_a]
        right = keys[pygame.K_d]
        down = keys[pygame.K_s]
        up = keys[pygame.K_w]
        mouse_pressed = pygame.mouse.get_pressed()
        move = pygame.math.Vector2(right - left, down -up)
        self.move_x = move.x
        self.move_y = move.y
        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            self.rect.move_ip(round(move.x), round(move.y))
            


        if mouse_pressed[0] and not self.mouse_button_pressed:
            self.shoot()
        
        # Update the mouse button state
        self.mouse_button_pressed = mouse_pressed[0]


        if keys[pygame.K_r]:
            
            self.weapon.play_reload_sound()
            self.reload_timer = pygame.time.get_ticks()

        self.update_walk_animation()

        for bullet in bullet_list:  
            self.boolet_delay(bullet)
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)



    def shoot(self):
        
        if self. shoot_cooldown == 0 and self.mag > 0 and self.reload == False:
            self.shoot_cooldown = 10
            pos = pygame.mouse.get_pos()
            barrel_offset_x = 10  
            barrel_offset_y = -5  
            mouse_x = pos[0]
            mouse_y = pos[1]

            if mouse_x < self.rect.centerx:
                barrel_offset_x *= -1
                barrel_offset_y *= -1
            barrel_offset = pygame.math.Vector2(barrel_offset_x, barrel_offset_y).rotate(self.orbit_angle)



            barrel_x = self.weapon.rect.centerx + barrel_offset.x

 
            barrel_y = self.weapon.rect.centery + barrel_offset.y
            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(barrel_x, barrel_y, mouse_x, mouse_y)

            # Add the bullet to the lists

            self.mag -= 1

            bullet_list.add(bullet)
            self.weapon.play_shot_sound()
            


        self.weapon.play_dry_fire_sound(self.mag)


    def boolet_delay(self, bullet):
        if self.shoot_cooldown == 9:
            bullet.image, bullet.rect = load_image("boolet.png", -1)
            

    def update_walk_animation(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]


        # Animate walking based on mouse position
        if self.move_x < 0:
            self.image = self.walk_left_frames[(pygame.time.get_ticks() // 150) % len(self.walk_left_frames)]
        elif self.move_x > 0:
            self.image = self.walk_right_frames[(pygame.time.get_ticks() // 150) % len(self.walk_right_frames)]
        elif self.move_y != 0:
            if mouse_x < self.rect.centerx:
                self.image = self.walk_left_frames[(pygame.time.get_ticks() // 150) % len(self.walk_left_frames)]
            else:
                self.image = self.walk_right_frames[(pygame.time.get_ticks() // 150) % len(self.walk_right_frames)]
        else:
            if mouse_x < self.rect.centerx:
                self.image = self.walk_left_frames[0]
            else:
                self.image = self.walk_right_frames[0]

            


    
    def update_weapon(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]

        mouse_offset = ((mouse_pos[0] - self.rect.centerx), (mouse_pos[1] - self.rect.centery))
        self.orbit_angle = math.degrees(math.atan2(mouse_offset[1], mouse_offset[0]))
        mouse_angle = -math.degrees(math.atan2(mouse_offset[1], mouse_offset[0]))

    # Set the initial weapon position relative to the player
        orbit_radius = 15
        weapon_center_x = self.rect.centerx + round(orbit_radius * math.cos(math.radians(self.orbit_angle)))
        weapon_center_y = self.rect.centery + round(orbit_radius * math.sin(math.radians(self.orbit_angle)))

        if mouse_x < self.rect.centerx:
            self.weapon.image = self.weapon.image_flipped
        else:
            self.weapon.image = self.weapon.image_unflipped

    # Rotate the weapon image
        rotated_weapon_image = rotate_on_pivot(self.weapon.image, mouse_angle)
    # Update the weapon's image and rect
        self.weapon.image = rotated_weapon_image
        self.weapon.rect = rotated_weapon_image.get_rect(center=(weapon_center_x, weapon_center_y))

            
    def update(self):
        
        self.input_or_movement()

        self.update_weapon()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.reload_timer > 0 and pygame.time.get_ticks() - self.reload_timer >= 3000:  
            self.mag = 6  # Set mag to 6 after the reload delay
            self.reload_timer = 0  # Reset the timer

        

 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """
 
    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set up the image for the bullet
        self.image, self.rect = load_image("boolet_inv.png", -1)
 
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
        velocity = 10
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
 
        # If the bullet flies off the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


class Player_Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.shot = shot_sound
        self.reload = reload_sound
        self.dry_fire = dry_fire_sound
        
        self.image_orig, self.rect = load_image("revolver.png", -1)


        self.image_unflipped = self.image_orig
        self.image_flipped = pygame.transform.flip(self.image_orig, False, True)
        
        self.image = self.image_orig



    def play_shot_sound(self):
        # Play the shot sound
        self.shot.play()

    def play_reload_sound(self):
        # Play the reload sound
        self.reload.play()

    def play_dry_fire_sound(self, mag):
        if mag == 0:
            self.dry_fire.play()
        else:
            pass

