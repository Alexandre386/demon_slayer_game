import pygame, os


class Tanjiro(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur=64, hauteur=55):
        super().__init__()

        self.frames = {}
        self.largeur = largeur
        self.hauteur = hauteur

        # Ajouter les frames
        self.add_frame("run1", "sprites/tanjiro3.png")
        self.add_frame("run2", "sprites/tanjiro2.png")
        self.add_frame("jump", "sprites/tanjiro1.png")

        # Redimensionner et retourner toutes les frames
        for key in self.frames:
            self.frames[key] = pygame.transform.scale(
                self.frames[key], (self.largeur, self.hauteur)
            )
            self.frames[key] = pygame.transform.flip(self.frames[key], True, False)

        # Frame initiale
        self.image = self.frames["run1"]
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Hitbox légèrement plus petite que le sprite
        marge_x = 18  # pixels à enlever sur les côtés
        marge_y = 15  # pixels à enlever en haut et bas
        self.hitbox = pygame.Rect(
            self.rect.left + marge_x,
            self.rect.top + marge_y,
            self.largeur - 2 * marge_x,
            self.hauteur - 2 * marge_y,
        )

        # Physique du saut
        self.vitesse_y = 0
        self.gravite = 1
        self.saut_force = -18
        self.au_sol = True
        self.sol_y = y

        # Animation course
        self.current_run_index = 0
        self.run_speed = 0.1
        self.run_order = ["run1", "run2"]

    # Ajouter une frame
    def add_frame(self, name, path):
        chemin = os.path.join(os.path.dirname(__file__), path)
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Image introuvable : {chemin}")
        self.frames[name] = pygame.image.load(chemin).convert_alpha()

    def update(self):
        # Gravité
        self.vitesse_y += self.gravite
        self.rect.y += self.vitesse_y

        # Hitbox suit le sprite
        marge_x = 8
        marge_y = 5
        self.hitbox.topleft = (self.rect.left + marge_x, self.rect.top + marge_y)

        if self.rect.bottom >= self.sol_y:
            self.rect.bottom = self.sol_y
            self.vitesse_y = 0
            self.au_sol = True
        else:
            self.au_sol = False

        # Animation
        if self.au_sol:
            self.current_run_index += self.run_speed
            if self.current_run_index >= len(self.run_order):
                self.current_run_index = 0
            self.image = self.frames[self.run_order[int(self.current_run_index)]]
        else:
            self.image = self.frames["jump"]

    def saut(self):
        if self.au_sol:
            self.vitesse_y = self.saut_force
            self.au_sol = False
