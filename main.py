import random

import pygame
import sys
from random import randint


def draw_bg():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + 1200, 0))


def create_cactus():
    cactus_rect = cactus_surface.get_rect(midtop=(1200, 455))
    return cactus_rect


def move_cactus(cactus):
    for n in cactus:
        n.centerx -= 4

    return cactus


def draw_cactus(cactuses):
    for cactus in cactuses:
        screen.blit(cactus_surface, cactus)


def check_collision(cactuses):
    for cactus in cactuses:
        if dinosaur_rect.colliderect(cactus):
            return False
    return True


def score_display():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(600, 20))
    screen.blit(score_surface, score_rect)


def final_score():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(600, 300))
    screen.blit(score_surface, score_rect)


def rotated_dinosaur(dinosaur):
    new_dinosaur = pygame.transform.rotozoom(dinosaur, -dinosaur_movement * 3, 1)
    return new_dinosaur


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Roboto', 45)

bg_surface = pygame.image.load('desert.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (1200, 600))

dinosaur_surface = pygame.image.load('dinosaur_game.png').convert_alpha()
dinosaur_surface = pygame.transform.scale(dinosaur_surface, (80, 100))
dinosaur_rect = dinosaur_surface.get_rect(center=(100, 560))

cactus_surface = pygame.image.load('cactus_game.png').convert_alpha()
cactus_surface = pygame.transform.scale(cactus_surface, (120, 150))
cactus_list = []
SPAWNCACTUS = pygame.USEREVENT

gravity = .12
dinosaur_movement = 0

bg_x_pos = 0
score = 0

game_active = True

while True:

    for event in pygame.event.get():
        cactus_g = [1400, 1800, 2000, 2500, 800, 1200, 2400]
        cactus_genarator = random.choice(cactus_g)
        pygame.time.set_timer(SPAWNCACTUS, cactus_genarator)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWNCACTUS:
            cactus_list.append(create_cactus())
            # print(cactus_list)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if dinosaur_rect.centery == 560:
                    dinosaur_movement = 0
                    dinosaur_movement -= 7

        if event.type == pygame.KEYDOWN:
            if event.key is pygame.K_BACKSPACE and game_active is False:
                game_active = True
                cactus_list.clear()
                dinosaur_rect.center = (80, 560)
                dinosaur_movement = 0
                score = 0

    bg_x_pos -= 1
    draw_bg()
    if bg_x_pos <= -1200:
        bg_x_pos = 0

    dinosaur_movement += gravity
    dinosaur_rect.centery += dinosaur_movement
    # dinosaur_rotated = rotated_dinosaur(dinosaur_surface)
    if game_active is True:
        if dinosaur_rect.centery >= 560:
            dinosaur_rect.centery = 560
            screen.blit(dinosaur_surface, dinosaur_rect)

        else:
            screen.blit(dinosaur_surface, dinosaur_rect)

        cactus_list = move_cactus(cactus_list)
        draw_cactus(cactus_list)
        game_active = check_collision(cactus_list)
        score += .01
        score_display()
    else:
        final_score()
    pygame.display.update()
    clock.tick(120)
