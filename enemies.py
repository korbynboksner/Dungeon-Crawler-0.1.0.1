import pygame, random
from ext import*
from character import*
from projectile import*
from extras import*



enemies_list = pygame.sprite.Group()


class Cultist(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.walk_left_frames = [load_image(f"cultist_walk_left_{i}.png", -1)[0] for i in range(1, 4)]
        self.walk_right_frames = [load_image(f"cultist_walk_right_{i}.png", -1)[0] for i in range(1, 4)]
        self.image = self.walk_right_frames[0]
        self.rect = self.image.get_rect()
        self.direction_facing_left = True
        self.movement_cooldown = 0
        self.fire_cooldown = 0
        self.moving = False
        self.health = 10
        self.move_x = 0
        self.move_y = 0
        self.rect.x = x
        self.rect.y = y

    def move_towards_player(self, player_rect):
        direction = pygame.math.Vector2(player_rect.centerx - self.rect.centerx, player_rect.centery - self.rect.centery)
        distance = direction.length()

        if distance > 0:
            direction.scale_to_length(random.uniform(2,5))
            direction.rotate_ip(random.uniform(-30, 30))
            self.move_x = direction.x
            self.move_y = direction.y
            self.rect.move_ip(direction)






    def update(self, player_rect, player_bullet_list):
        if self.movement_cooldown <= 0:
            self.move_towards_player(player_rect)
            self.movement_cooldown = 30
        
        self.update_walk_animation(player_rect)

        self.bullet_collisions(player_bullet_list)

        if self.fire_cooldown <= 0:
            self.fire_projectile(player_rect)
            self.fire_cooldown = 60  

        # Update cooldowns
        self.movement_cooldown -= 1
        self.fire_cooldown -= 1


    def fire_projectile(self, player_rect):
        

        if self.direction_facing_left:
            offset = (player_rect.centerx - self.rect.topleft[0]), (self.rect.topleft[1] - self.rect.centery)
            angle = -math.degrees(math.atan2(offset[1], offset[0]))
            


            spell = Acid_spell(self.rect.topleft[0], self.rect.topleft[1], player_rect.centerx, player_rect.centery)
        else:
            offset = (player_rect.centerx - self.rect.topright[0]), (self.rect.topright[1] - self.rect.centery)
            angle = -math.degrees(math.atan2(offset[1], offset[0]))
            


            spell = Acid_spell(self.rect.topright[0], self.rect.topright[1], player_rect.centerx, player_rect.centery)

        if player_rect.centerx < self.rect.centerx:
            rotated_image, rotated_rect = self.rotate_spell(spell.image_orig, angle)
            flipped_image = pygame.transform.flip(rotated_image, False, True)  # Flip the rotated image horizontally
            spell.image = flipped_image
            spell.rect = rotated_rect
            
        else:
            rotated_image, rotated_rect = spell.rotate_spell(spell.image_orig, angle)
            spell.image = rotated_image
            spell.rect = rotated_rect
            
        projectile_list.add(spell)


    def rotate_spell(self, image, angle):
        image_rect = image.get_rect()
        center = image_rect.center

        rotated_image = pygame.transform.rotate(image, angle)

        rotated_rect = rotated_image.get_rect(center=center)

        return rotated_image, rotated_rect

    def update_walk_animation(self, player_rect):
        if self.move_x < 0:
            self.image = self.walk_left_frames[(pygame.time.get_ticks() // 150) % len(self.walk_left_frames)]
            self.direction_facing_left = True
        elif self.move_x > 0:
            self.image = self.walk_right_frames[(pygame.time.get_ticks() // 150) % len(self.walk_right_frames)]
            self.direction_facing_left = False
        elif self.move_y != 0:
            if player_rect.centerx < self.rect.centerx:
                self.image = self.walk_left_frames[(pygame.time.get_ticks() // 150) % len(self.walk_left_frames)]
                self.direction_facing_left = True
            else:
                self.image = self.walk_right_frames[(pygame.time.get_ticks() // 150) % len(self.walk_right_frames)]
                self.direction_facing_left = False
        else:
            if player_rect.centerx < self.rect.centerx:
                self.image = self.walk_left_frames[0]
                self.direction_facing_left = True
            else:
                self.image = self.walk_right_frames[0]
                self.direction_facing_left = False

    def bullet_collisions(self, player_bullet_list):
        
        hits = pygame.sprite.spritecollide(self, player_bullet_list, True)
        if hits:
            self.health -= 1
        if self.health <= 0:
            # The cultist is defeated
            enemies_list.remove(self)
