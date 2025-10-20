import pygame, sys
from tanjiro import Tanjiro
from map import Map

pygame.init()

# Fenêtre
LARGEUR, HAUTEUR = 800, 400
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Demon Slayer Runner")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

def jeu():
    game_map = Map(LARGEUR, HAUTEUR, "sprites/arriere_plans.png")
    tanjiro = Tanjiro(50, game_map.sol_y)
    perso_group = pygame.sprite.GroupSingle(tanjiro)

    score = 0
    dernier_pallier = 0

    # Boost
    boost_actif = False
    boost_fin = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tanjiro.saut()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tanjiro.saut()

        # Update
        perso_group.update()
        game_map.update()

        # Vérif boost expiré
        if boost_actif and pygame.time.get_ticks() > boost_fin:
            boost_actif = False

        # Collision
        collision = False
        for obs in game_map.obstacles[:]:
            if tanjiro.hitbox.colliderect(obs["hitbox"]):
                if obs["type"] == "powerup":
                    boost_actif = True
                    boost_fin = pygame.time.get_ticks() + 10000  # 10s
                    game_map.obstacles.remove(obs)
                elif obs["type"] == "obstacle":
                    if boost_actif:
                        game_map.obstacles.remove(obs)
                        score += 50  # bonus destruction
                    else:
                        collision = True
                        break

        # Score
        score += 2 if boost_actif else 1

        # Accélération
        pallier = score // 1500
        if pallier > dernier_pallier:
            tanjiro.run_speed += 0.1
            game_map.bg_speed += 0.5
            game_map.obstacle_speed += 0.5
            dernier_pallier = pallier

        # Affichage
        fenetre.fill((150, 200, 255))
        game_map.draw(fenetre)
        perso_group.draw(fenetre)

        # Score
        txt = f"Score : {score}" + (" (BOOST)" if boost_actif else "")
        fenetre.blit(font.render(txt, True, (0, 0, 0)), (10, 10))

        pygame.display.flip()
        clock.tick(60)

        if collision:
            return score

# Boucle principale
while True:
    score_final = jeu()

    # Écran de fin
    fenetre.fill((0, 0, 0))
    msg1 = font.render(f"Game Over ! Score : {score_final}", True, (255, 255, 255))
    msg2 = font.render("Appuyez sur ESPACE pour rejouer", True, (255, 255, 255))
    fenetre.blit(msg1, (LARGEUR//2 - msg1.get_width()//2, HAUTEUR//2 - 30))
    fenetre.blit(msg2, (LARGEUR//2 - msg2.get_width()//2, HAUTEUR//2 + 10))
    pygame.display.flip()

    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                attente = False
