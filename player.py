import pygame
pygame.init()

class Player():
    def __init__(self, surface, position_x, position_y, width, height):
        img1 = pygame.image.load("Missile_3_Flying_001.png").convert_alpha()
        img2 = pygame.image.load("Bomb_3_Explosion_000.png").convert_alpha()
        self.height = height
        self.width = width
        self.player_image = pygame.transform.scale(img1, (self.width, self.height))
        self.enemy_image = pygame.transform.scale(img2, (self.width, self.height))
        self.surface = surface
        self.position_x = position_x
        self.position_y = position_y
        self.rect = self.player_image.get_rect(topleft=(self.position_x, self.position_y))
        self.rect2 = self.enemy_image.get_rect(topleft=(self.position_x, self.position_y))
        self.player_mask = pygame.mask.from_surface(self.player_image)
        self.enemy_mask = pygame.mask.from_surface(self.enemy_image)

    def load_player(self):
        self.surface.blit(self.player_image, self.rect)

    def load_enemy(self):
        self.surface.blit(self.enemy_image, self.rect2)



def write(font,text, screen, font_size,posx,posy,color):
    font = pygame.font.SysFont(font, font_size, bold=False, italic=False)
    surface = font.render(text,True, color)
    screen.blit(surface,(posx,posy))



 


        