import pygame, random


screen_height = 650
screen_width =500

class Coin:
    def __init__(self,surface, xposition, yposition):
        img = pygame.image.load("Damage_Bonus.png").convert_alpha()
        self.coin_image = pygame.transform.scale(img, (30, 30))
        self.surface = surface
        self.xpostion = xposition
        self.yposition = yposition
        self.rect = self.coin_image.get_rect(topleft=(self.xpostion, self.yposition))
        self.coin_mask = pygame.mask.from_surface(self.coin_image)

    def load_coin(self):
        self.surface.blit(self.coin_image, self.rect)

class Health:
    def __init__(self,surface,xposition,yposition):
        img = pygame.image.load("HP_Bonus.png").convert_alpha()
        self.health_image = pygame.transform.scale(img, (30, 30))
        self.surface = surface
        self.xpostion = xposition
        self.yposition = yposition
        self.rect = self.health_image.get_rect(topleft=(self.xpostion, self.yposition))
        self.health_mask = pygame.mask.from_surface(self.health_image)
    
    def load_health(self):
        self.surface.blit(self.health_image,(self.rect))

    def hide_health(self):
        self.rect.x = 30 + screen_width

class Shield:
    def __init__(self, surface, xposition, yposition):
        img = pygame.image.load("Armor_Bonus.png").convert_alpha()
        self.shield_image = pygame.transform.scale(img, (30, 30))
        self.surface = surface
        self.xpostion = xposition
        self.yposition = yposition
        self.rect = self.shield_image.get_rect(topleft=(self.xpostion, self.yposition))
        self.shield_mask = pygame.mask.from_surface(self.shield_image)

    def load_shield(self):
        self.surface.blit(self.shield_image,(self.rect))

    def hide_shield(self):
        self.rect.x = 30 + screen_width
