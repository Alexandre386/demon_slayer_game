import sys

import pygame

from map import Map
from tanjiro import Tanjiro

pygame.init()

# Fenêtre
LARGEUR, HAUTEUR = 800, 400
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Demon Slayer Runner")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# Games settings
BUFF_BOOST_FACTOR = 5

starting_time = pygame.time.get_ticks()


def jeu():
    # Création du décor et du personnage
    game_map = Map(LARGEUR, HAUTEUR, "sprites/arriere_plans.png")
    tanjiro = Tanjiro(50, game_map.sol_y)
    perso_group = pygame.sprite.GroupSingle(tanjiro)

    score = 0
    dernier_pallier = 0
    last_buff_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tanjiro.saut()

        # Update
        perso_group.update()
        game_map.update()

        # Collision/Buff
        collision = False
        for obs in game_map.obstacles:
            if tanjiro.hitbox.colliderect(obs["rect"]):
                if obs["type"] == "buff":
                    last_buff_time = pygame.time.get_ticks()
                    break
                else:
                    collision = True
                    break

        buff = False
        print(last_buff_time)
        print(pygame.time.get_ticks() - last_buff_time)
        if last_buff_time and (pygame.time.get_ticks() - last_buff_time) < 5000:
            buff = True

        # Score
        if buff:
            score += 1 * BUFF_BOOST_FACTOR
        else:
            score += 1

        # Accélération tous les 1500 points
        pallier = score // 1500
        if pallier > dernier_pallier:
            tanjiro.run_speed += 0.1
            game_map.bg_speed += 0.5
            game_map.obstacle_speed += 0.5
            dernier_pallier = pallier

        # Affichage
        fenetre.fill((150, 200, 255))  # fond
        game_map.draw(fenetre)
        perso_group.draw(fenetre)

        # Score
        if buff:
            score_surf = font.render(f"Score : {score}", True, (255, 255, 0))
        else:
            score_surf = font.render(f"Score : {score}", True, (0, 0, 0))
        fenetre.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        # Game over
        if collision:
            return score


# Boucle principale
while True:
    score_final = jeu()

    # Écran de fin
    fenetre.fill((0, 0, 0))
    msg_surf = font.render(f"Game Over ! Score : {score_final}", True, (255, 255, 255))
    msg_relaunch = font.render("Appuyez sur ESPACE pour rejouer", True, (255, 255, 255))
    fenetre.blit(
        msg_surf, (LARGEUR // 2 - msg_surf.get_width() // 2, HAUTEUR // 2 - 30)
    )
    fenetre.blit(
        msg_relaunch, (LARGEUR // 2 - msg_relaunch.get_width() // 2, HAUTEUR // 2 + 10)
    )
    pygame.display.flip()

    # Attente de relance
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attente = False  # relancer le jeu
