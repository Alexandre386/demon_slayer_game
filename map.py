import os
import random

import pygame


class Map:
    def __init__(self, largeur, hauteur, sprite_fond=None):
        """
        Initialise la map avec fond et obstacles.
        """
        self.largeur = largeur
        self.hauteur = hauteur

        # Liste des obstacles
        self.obstacles = []

        # Timer pour générer les obstacles
        self.last_spawn = pygame.time.get_ticks()
        self.obstacle_interval = 1200
        self.spawn_delay = 2000

        # Chances a buff obstacle will spawn
        self.buff_spawn_chance = 5

        # Chances a demon obstacle will spawn
        self.demon_spawn_chance = 20

        # --- Fond ---
        if sprite_fond:
            chemin_fond = os.path.join(os.path.dirname(__file__), sprite_fond)
            if not os.path.exists(chemin_fond):
                raise FileNotFoundError(f"Image de fond introuvable : {chemin_fond}")
            self.background = pygame.image.load(chemin_fond).convert()
            self.background = pygame.transform.scale(
                self.background, (largeur, hauteur)
            )

            # Position du sol proportionnelle à l'image originale
            sol_original = 1000  # y du sol dans l'image originale
            self.sol_y = int(sol_original * (self.hauteur / 1300))
        else:
            self.background = None
            self.sol_y = self.hauteur - 50

        # Défilement
        self.bg_x = 0
        self.bg_speed = 5.0  # vitesse de base du fond

        # --- Charger textures d'obstacles ---
        self.obstacle_textures = []
        textures = ["tronc.png", "rocher.png", "barile.png"]
        for tex in textures:
            chemin_tex = os.path.join(
                os.path.dirname(__file__), "sprites", "Obstacles", tex
            )
            if os.path.exists(chemin_tex):
                img = pygame.image.load(chemin_tex).convert_alpha()
                self.obstacle_textures.append(img)
            else:
                print(f"⚠️ Texture d'obstacle introuvable : {chemin_tex}")

        # --- Load obstacle buff texture ---
        chemin_tex = os.path.join(
            os.path.dirname(__file__),
            "sprites",
            "Obstacles",
            "nezuko.png",
        )
        if os.path.exists(chemin_tex):
            img = pygame.image.load(chemin_tex).convert_alpha()
            self.obstacle_buff_texture = img
        else:
            print(f"⚠️ Texture d'obstacle introuvable : {chemin_tex}")

        # --- Load obstacle demon texture ---
        chemin_tex = os.path.join(
            os.path.dirname(__file__),
            "sprites",
            "Obstacles",
            "demon2.png",
        )
        if os.path.exists(chemin_tex):
            img = pygame.image.load(chemin_tex).convert_alpha()
            self.obstacle_demon_texture = img
        else:
            print(f"⚠️ Texture d'obstacle demon introuvable : {chemin_tex}")

    def spawn_obstacle(self):
        """
        Crée un nouvel obstacle à droite de l'écran avec taille aléatoire.
        """

        if random.randrange(0, 100) <= self.buff_spawn_chance:
            # Handle buff obstacle
            texture = self.obstacle_buff_texture
            h = 50
            ratio = h / texture.get_height()
            w = int(texture.get_width() * ratio)
            texture_redim = pygame.transform.scale(texture, (w, h))

            # Rect aligné au sol
            rect = texture_redim.get_rect(bottomleft=(self.largeur, self.sol_y))
            self.obstacles.append(
                {
                    "image": texture_redim,
                    "rect": rect,
                    "type": "buff",
                    "x": float(rect.x),
                }
            )

        elif random.randrange(0, 100) <= self.demon_spawn_chance:
            # Handle demon obstacle
            texture = self.obstacle_demon_texture
            h = 60
            ratio = h / texture.get_height()
            w = int(texture.get_width() * ratio)
            texture_redim = pygame.transform.scale(texture, (w, h))

            # Rect aligné au sol
            rect = texture_redim.get_rect(bottomleft=(self.largeur, self.sol_y))
            self.obstacles.append(
                {
                    "image": texture_redim,
                    "rect": rect,
                    "type": "demon",
                    "x": float(rect.x),
                }
            )

        else:
            # Handle normal obstacle
            if self.obstacle_textures:
                texture = random.choice(self.obstacle_textures)

                # Hauteur aléatoire
                h = random.randint(50, 70)
                ratio = h / texture.get_height()
                w = int(texture.get_width() * ratio)
                texture_redim = pygame.transform.scale(texture, (w, h))

                # Rect aligné au sol
                rect = texture_redim.get_rect(bottomleft=(self.largeur, self.sol_y))
                self.obstacles.append(
                    {
                        "image": texture_redim,
                        "rect": rect,
                        "type": "obstacle",
                        "x": float(rect.x),
                    }
                )
            else:
                # fallback rectangle
                w, h = random.randint(30, 70), random.randint(30, 70)
                x = self.largeur
                y = self.sol_y - h
                color = random.choice([(139, 69, 19), (128, 0, 0), (105, 105, 105)])
                self.obstacles.append(
                    {
                        "rect": pygame.Rect(x, y, w, h),
                        "color": color,
                        "type": "obstacle",
                    }
                )

    def update(self):
        """
        Met à jour la position des obstacles et du fond.
        """
        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.obstacle_interval and now > self.spawn_delay:
            self.spawn_obstacle()
            self.last_spawn = now

        for obs in self.obstacles:
            obs["x"] -= self.bg_speed
            obs["rect"].x = int(obs["x"])

        # Supprimer obstacles sortis de l'écran
        self.obstacles = [obs for obs in self.obstacles if obs["rect"].right > 0]

        # Défilement du fond
        if self.background:
            self.bg_x -= self.bg_speed
            if self.bg_x <= -self.largeur:
                self.bg_x += self.largeur

    def draw(self, surface):
        """
        Dessine le fond et les obstacles sur la surface.
        """
        # # Fond
        if self.background:
            surface.blit(self.background, (self.bg_x, 0))
            surface.blit(self.background, (self.bg_x + self.largeur, 0))
        else:
            surface.fill((135, 206, 250))  # ciel bleu par défaut

        # Dessiner obstacles
        for obs in self.obstacles:
            if "image" in obs:
                surface.blit(obs["image"], obs["rect"].topleft)
            else:
                pygame.draw.rect(surface, obs["color"], obs["rect"])
