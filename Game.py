# Example file showing a circle moving on screen
import pygame
# import exit from sys library
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = score.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(midright=(960, 30))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movment(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8

            if obstacle_rect.bottom == 529:
                screen.blit(stake,obstacle_rect)
            else:
                screen.blit(bullet, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -170]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# initializing pygame
pygame.init()
# creating screen and making is 960 by 600
screen = pygame.display.set_mode((960, 600))
# set the caption of the task bar
pygame.display.set_caption("SkullCat")
# initialize the clock variable
clock = pygame.time.Clock()
# initializing the font and size of the text; None means the default font
score = pygame.font.Font('Fonts/Pixeltype.ttf', 50)
title = pygame.font.Font('Fonts/Pixeltype.ttf', 200)
game_active = True
game_start = True
start_time = 0
final_score = 0

# importing images and .convert_alpha is converting the pngs to a format
# that pygame can read easier
test_surface = pygame.image.load('images/orange.png').convert_alpha()
ground = pygame.image.load('images/ground.png').convert_alpha()
end_background = pygame.image.load('images/blue_sky.png').convert_alpha()
end_background_scaled = pygame.transform.rotozoom(end_background, 0, 1.2)

# text_surface = score.render('Score', False, (64, 64, 64)).convert_alpha()
# text_rect = text_surface.get_rect(center=(480, 30))

# obstacles
stake = pygame.image.load('images/stake.png').convert_alpha()

bullet = pygame.image.load('images/bullet.png').convert_alpha()

obstacle_rect_list = []

SkullCat = pygame.image.load('images/GIANT.png').convert_alpha()
angel_SkullCat = pygame.image.load('images/GIANT_ANGEL.png').convert_alpha()
player_rect = SkullCat.get_rect(bottomleft=(80, 529))
normal_angel_SkullCat = angel_SkullCat.get_rect(midbottom=(790, 529))
SkullCat_scaled = pygame.transform.rotozoom(angel_SkullCat, 0, 1.5)
game_over_player_rect = SkullCat_scaled.get_rect(center=(480, 300))
player_gravity = 0

title_text = title.render(f'Skull Cat', False, 'Black')
title_rect = title_text.get_rect(center=(480, 100))

start_button = score.render(f'Start', False, 'Black')
start_button_rect = start_button.get_rect(midbottom=(480, 529))

game_name = score.render('SkullCat is Dead!', False, 'Black')
game_name_rect = game_name.get_rect(midbottom=(480, 50))

game_message = score.render('Press space to run again', False, 'Black')
game_message_rect = game_message.get_rect(midtop=(480, 500))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 3000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_start:
            game_active = False
            screen.blit(test_surface, (0, 0))
            screen.blit(ground, (0, 529))
            screen.blit(SkullCat, player_rect)
            screen.blit(angel_SkullCat, normal_angel_SkullCat)
            screen.blit(title_text, title_rect)
            screen.blit(start_button, start_button_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                game_start = False

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -30

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 529:
                    player_gravity = -30
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(stake.get_rect(bottomleft=(randint(960,1100), 529)))
            else:
                obstacle_rect_list.append(bullet.get_rect(bottomleft=(randint(960,1100), 280)))

    if game_active:
        screen.blit(test_surface, (0, 0))
        screen.blit(ground, (0, 529))
        # use rect to move objects instead of the surface itself
        # player_rect.left += 1
        # screen.blit(text_surface, text_rect)
        # final_score = display_score()
        # stake_rect.left -= 10
        # if stake_rect.right <= 0:
            # stake_rect.left = 960

        # screen.blit(stake, stake_rect)

        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >= 529:
            player_rect.bottom = 529

        screen.blit(SkullCat, player_rect)

        # Obstacle movment
        obstacle_rect_list = obstacle_movment(obstacle_rect_list)
        

        # basically saying if player_rect.colliderect(stake_rect) == 1 but 0 is automatically false so no need
        # if player_rect.colliderect(stake_rect):
        # print("w")

        # collision
        game_active = collisions(player_rect, obstacle_rect_list) 

    elif (game_active == False) and (game_start == False):
        screen.blit(end_background_scaled, (0, 0))
        screen.blit(SkullCat_scaled, game_over_player_rect)
        obstacle_rect_list.clear()
        player_rect.bottomleft = (80, 529)
        player_gravity = 0

        # animation to make the skull angel go from top to bottom on the screen
        game_over_player_rect.top -= 5
        if game_over_player_rect.bottom <= 0:
            game_over_player_rect.top = 600

        final_score_message = score.render(f'Your final score: {final_score}', False, 'Black')
        final_score_message_rect = final_score_message.get_rect(midtop=(480, 550))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(final_score_message, final_score_message_rect)

    pygame.display.update()
    clock.tick(60)
