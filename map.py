import pygame, os, random

class Map:
    def __init__(self, largeur, hauteur, sprite_fond=None):
        self.largeur = largeur
        self.hauteur = hauteur
        self.obstacles = []

        # Timer
        self.last_spawn = pygame.time.get_ticks()
        self.obstacle_interval = 1200
        self.spawn_delay = 2000

        # Fond
        if sprite_fond:
            chemin_fond = os.path.join(os.path.dirname(__file__), sprite_fond)
            if not os.path.exists(chemin_fond):
                raise FileNotFoundError(f"Image de fond introuvable : {chemin_fond}")
            self.background = pygame.image.load(chemin_fond).convert()
            self.background = pygame.transform.scale(self.background, (largeur, hauteur))
            sol_original = 1000
            self.sol_y = int(sol_original * (hauteur / 1300))
        else:
            self.background = None
            self.sol_y = hauteur - 50

        self.bg_x = 0
        self.bg_speed = 5
        self.obstacle_speed = 5

        # Textures obstacles
        self.obstacle_textures = []
        textures = ["tronc.png", "rocher.jpeg", "barile.jpeg"]
        for tex in textures:
            chemin_tex = os.path.join(os.path.dirname(__file__), "sprites", "Obstacles", tex)
            if os.path.exists(chemin_tex):
                img = pygame.image.load(chemin_tex).convert_alpha()
                self.obstacle_textures.append(img)
            else:
                print(f"⚠️ Texture d'obstacle introuvable : {chemin_tex}")

        # Texture du power-up (facultatif)
        powerup_path = os.path.join(os.path.dirname(__file__), "sprites", "nezuko.png")
        if os.path.exists(powerup_path):
            self.powerup_texture = pygame.image.load(powerup_path).convert_alpha()
        else:
            self.powerup_texture = None
            print("⚠️ Aucun powerup trouvé (sprites/nezuko.png) → il ne sera pas utilisé.")

    def spawn_powerup(self):
        """ Crée un power-up si une texture existe """
        if self.powerup_texture:
            tex = pygame.transform.scale(self.powerup_texture, (40, 40))
            rect = tex.get_rect(midbottom=(self.largeur + 20, self.sol_y - 30))
            self.obstacles.append({
                "image": tex,
                "rect": rect.copy(),
                "hitbox": rect.copy(),
                "type": "powerup"
            })

    def spawn_obstacle(self):
        """ 80% obstacle, 20% powerup """
        if self.powerup_texture and random.random() < 20:  # 20% seulement si texture existe
            self.spawn_powerup()
            return

        if not self.obstacle_textures:
            # Fallback rectangle
            w, h = random.randint(30, 70), random.randint(30, 70)
            x = self.largeur
            y = self.sol_y - h
            color = random.choice([(139,69,19), (128,0,0), (105,105,105)])
            self.obstacles.append({
                "rect": pygame.Rect(x, y, w, h),
                "color": color,
                "type": "obstacle"
            })
            return

        # Choisir une texture et la redimensionner
        texture = random.choice(self.obstacle_textures)
        h = random.randint(50, 90)
        ratio = h / texture.get_height()
        w = int(texture.get_width() * ratio)
        texture_redim = pygame.transform.scale(texture, (w, h))

        rect = texture_redim.get_rect(midbottom=(self.largeur + w//2, self.sol_y))
        self.obstacles.append({
            "image": texture_redim,
            "rect": rect.copy(),
            "hitbox": rect.copy(),
            "type": "obstacle"
        })

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.obstacle_interval and now > self.spawn_delay:
            self.spawn_obstacle()
            self.last_spawn = now

        for obs in self.obstacles:
            obs["rect"].x -= self.obstacle_speed
            obs["hitbox"].x = obs["rect"].x
            obs["hitbox"].y = obs["rect"].y

        # Supprimer les hors-écran
        self.obstacles = [o for o in self.obstacles if o["rect"].right > 0]

        # Boucle fond
        if self.background:
            self.bg_x -= self.bg_speed
            if self.bg_x <= -self.largeur:
                self.bg_x = 0

    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (self.bg_x, 0))
            surface.blit(self.background, (self.bg_x + self.largeur, 0))
        else:
            surface.fill((135,206,250))

        for obs in self.obstacles:
            if "image" in obs:
                surface.blit(obs["image"], obs["rect"].topleft)
            else:
                pygame.draw.rect(surface, obs["color"], obs["rect"])
