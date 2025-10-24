import pygame, os


class Tanjiro(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur=50, hauteur=47):
        super().__init__()

        self.frames = {}
        self.largeur = largeur
        self.hauteur = hauteur
        self.attack_largeur = 57
        self.attack_hauteur = 54

        # Ajouter les frames
        self.add_frame("run1", "sprites/run1.png", False)
        self.add_frame("run2", "sprites/run2.png", False)
        self.add_frame("run3", "sprites/run3.png", False)
        self.add_frame("run4", "sprites/run4.png", False)
        self.add_frame("run5", "sprites/run5.png", False)
        self.add_frame("run6", "sprites/run6.png", False)
        self.add_frame("jump1", "sprites/jump1.png", False)
        self.add_frame("jump2", "sprites/jump2.png", False)
        self.add_frame("attack1", "sprites/attack1.png", True)
        self.add_frame("attack2", "sprites/attack2.png", True)
        self.add_frame("attack3", "sprites/attack3.png", True)

        # Redimensionner toutes les frames
        for key in self.frames:
            pass

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

        # Attack
        self.current_attack_index = 0
        self.attack_speed = 0.15  # Lower = slower
        self.attack_order = ["attack1", "attack2", "attack3"]
        self.is_attacking = False

        # Jump
        self.current_jump_index = 0
        self.jump_speed = 0.15  # Lower = slower
        self.jump_order = ["jump1", "jump2"]

        # Physique du saut
        self.vitesse_y = 0
        self.gravite = 1
        self.saut_force = -18
        self.au_sol = True
        self.sol_y = y

        # Animation course
        self.current_run_index = 0
        self.run_speed = 0.1
        self.run_order = ["run1", "run2", "run3", "run4", "run5", "run6"]

    # Ajouter une frame
    def add_frame(self, name, path, is_attack=False):
        chemin = os.path.join(os.path.dirname(__file__), path)
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Image introuvable : {chemin}")
        img = pygame.image.load(chemin).convert_alpha()
        if is_attack:
            self.frames[name] = pygame.transform.scale(
                img, (self.attack_largeur, self.attack_hauteur)
            )
        else:
            self.frames[name] = pygame.transform.scale(
                img, (self.largeur, self.hauteur)
            )

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

        # Attack animation
        if self.is_attacking:
            self.current_attack_index += self.attack_speed
            if self.current_attack_index >= len(self.attack_order):
                self.is_attacking = False
                self.current_attack_index = 0
            else:
                self.image = self.frames[
                    self.attack_order[int(self.current_attack_index)]
                ]
        # Running animation
        elif self.au_sol:
            self.current_run_index += self.run_speed
            if self.current_run_index >= len(self.run_order):
                self.current_run_index = 0
            self.image = self.frames[self.run_order[int(self.current_run_index)]]
        # Jumping animation
        else:
            self.current_jump_index += self.jump_speed
            if self.current_jump_index >= len(self.jump_order):
                self.is_jumping = False
                self.current_jump_index = 0
            else:
                self.image = self.frames[self.jump_order[int(self.current_jump_index)]]

    def saut(self):
        if self.au_sol:
            self.vitesse_y = self.saut_force
            self.au_sol = False

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
