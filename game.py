import pygame, sys, random, json
from pygame.locals import *
from player import Player, write
from bonuses import Coin, Health, Shield

pygame.init()

#Music
pygame.mixer.init()
pygame.mixer.music.load("red-e-8-bit-chiptune-for-retro-gaming-356128.mp3")
pygame.mixer.music.play(-1)

#colors
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)

clock = pygame.time.Clock()

#screen
screen_height = 650
screen_width =500
screen = pygame.display.set_mode((screen_width,screen_height))
background_image = pygame.image.load("background_image.jfif")
scaled_background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

pygame.display.set_caption("space ranger")

game_state = "menu"
game_over = False


life = 3
score = 0


#player
player_xpostion = 200
player_yxpostion = 570
player_height = 60
player_width = 100
player_speed = 7
player = Player(screen,player_xpostion,player_yxpostion, player_width, player_height)


#enemy
enemy_width = 100
enemy_height = 60
enemy_xpostion = random.randint(0,screen_width - enemy_width)
enemy_ypostion = -enemy_height
enemies = [Player(screen, enemy_xpostion, enemy_ypostion, enemy_width, enemy_height)]
enemy_speed = 5
enemy_timer = 0
collision_timer = 0

#coin
xcoin = random.randint(0, screen_width-30)
ycoin = random.randint(0,screen_height - 30)
coin = Coin(screen,xcoin,ycoin)

#health
xhealth = random.randint(0, 130)
yhealth = random.randint(0,screen_height - 30)
health = Health(screen,xhealth,yhealth)  
health_showing = True
health_check_timer = 0

#shield
xshield = random.randint(260, screen_width-20)
yshield = random.randint(0,screen_height - 20)
shield = Shield(screen,xshield,yshield)  
shield_showing = True
shield_check_timer = 0
player_shielded = False
shield_activation_time = 0

#scores
score_saved = False
new_high_score = False

def save_high_score(score):
    try:
        with open('high_score.json','r') as file:
            high_score = json.load(file)
    except FileNotFoundError:
        high_score = 0
    if score > high_score:
        global new_high_score
        new_high_score = True
        with open('high_score.json','w') as file:
            json.dump(score,file)

def get_high_score():
    try:
        with open('high_score.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        return 0
    
def display_menu():
    write("comic sans","SPACE", screen, 80,50,100,white)
    write("comic sans","EXPLORER",screen,80,80,170,red)
    write("comic sans","press s to start",screen,40,50,240,green)




running = True
while running:
    screen.blit(scaled_background_image,(0,0))
    if game_state == "menu":
        display_menu()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_state == "playing":
                    game_state = "pause"
                elif game_state == "pause":
                    game_state = "playing"
            if event.key == K_RETURN:
                game_state = "start"
                game_over = False
            if event.key == K_s:
                game_state = "start"


# code for moving the player    
    keys = pygame.key.get_pressed()


    if game_state == "start":
        life = 4
        score = 0
        game_state = "playing"
        score_saved = False
        new_high_score = False

        
        

    if game_state == "playing":
        if keys[K_LEFT] and player.rect.x >= 0:
            player.rect.x -= player_speed
        elif keys[K_RIGHT] and player.rect.x <= screen_width - player.width:
            player.rect.x += player_speed
        elif keys[K_UP] and player.rect.y >= 0:
            player.rect.y -= player_speed
        elif keys[K_DOWN] and player.rect.y <= screen_height - player.height:
            player.rect.y += player_speed

# code for handling enemy
    for enemy in enemies:
        enemy_current_time = pygame.time.get_ticks()
        if enemy_current_time - enemy_timer > 1000 and len(enemies) < 7:
            enemies.append(Player(screen, enemy_xpostion, enemy_ypostion, enemy_width, enemy_height))
            enemy_timer = enemy_current_time
        if game_state == "playing" and score <=5:
            enemy.rect2.y += enemy_speed
        elif game_state == "playing" and score >= 5:
            enemy.rect2.y += enemy_speed +2
        if enemy.rect2.y >= screen_height:
            enemy.rect2.y = 0
            enemy.rect2.x = random.randint(0, screen_width-enemy_width)
        enemy.load_enemy()

        offset_x = enemy.rect2.x - player.rect.x
        offset_y = enemy.rect2.y - player.rect.y

        collision_current_time = pygame.time.get_ticks()
        if player.player_mask.overlap(enemy.enemy_mask, (offset_x, offset_y)) and \
                collision_current_time - collision_timer > 800:
            if life > 0 and not player_shielded:
                life -= 1
                collision_timer = collision_current_time

    if life <= 0:
        game_over = True




# code for handling coin 
    offset_x_coin = coin.rect.x - player.rect.x
    offset_y_coin = coin.rect.y - player.rect.y

    if player.player_mask.overlap(coin.coin_mask, (offset_x_coin, offset_y_coin)):
        score += 1
        coin.rect.x = random.randint(0, screen_width-30)
        coin.rect.y = random.randint(0, screen_height-30)


#code for handling health    
    if health_showing:
        health.load_health()
        offset_x_health = health.rect.x - player.rect.x
        offset_y_health = health.rect.y - player.rect.y

        if player.player_mask.overlap(health.health_mask, (offset_x_health, offset_y_health)):
            life += 1
            health.hide_health()
            health_showing = False


    health_current_time = pygame.time.get_ticks()
    if not health_showing:
        if health_current_time - health_check_timer > 3000:  
            if random.randint(1, 10) == 5:  
                health_showing = True
                health.rect.x = random.randint(0, 130)
                health.rect.y = random.randint(0, screen_height - 30)
            health_check_timer = health_current_time

#code for handling shield
    if shield_showing:
        shield.load_shield()
        offset_x_shield = shield.rect.x - player.rect.x
        offset_y_shield = shield.rect.y - player.rect.y

        if player.player_mask.overlap(shield.shield_mask, (offset_x_shield, offset_y_shield)):
            player_shielded = True
            shield_activation_time = pygame.time.get_ticks()
            shield.hide_shield()
            shield_showing = False


    if player_shielded:
        current_time = pygame.time.get_ticks()
        if current_time - shield_activation_time >= 5000:
            player_shielded = False


    shield_current_time = pygame.time.get_ticks()
    if not shield_showing:
        if shield_current_time - shield_check_timer > 3000:  
            if random.randint(1, 20) == 5:  
                shield_showing = True
                shield.rect.x = random.randint(260, screen_width-20)
                shield.rect.y = random.randint(0, screen_height - 30)
            shield_check_timer = shield_current_time


    write("arial",f"life: {life}", screen, 20,0,0,white)
    write("arial",f"score: {score}", screen,20,400,0,white)

    write("arial",f"High Score: {get_high_score()}", screen,20,0,screen_height-40,white)
    if player_shielded:
        write("arial","Shield", screen,20,200,0,green)
    
    if game_state == "pause" and not game_over:
        write("arial","PAUSE", screen, 50,150,230, white)
    
    if game_over:
        game_state = "pause"
        if not score_saved:
            save_high_score(score)
            score_saved=True

        write("arial","GAME OVER", screen, 50,100,230, red)
        write("arial","Press Enter to start again", screen,20,100,280,white)
        if new_high_score:
            write("arial","New High Score!!!", screen,40,100,310,green)
            
 

        
    clock.tick(60)
    player.load_player()
    coin.load_coin()
    
    pygame.display.update()
