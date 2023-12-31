import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += 1
        if self.rect.x > 600:
            self.rect.x = -3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player_1.png")
        self.scale_image = pygame.transform.scale(self.image, (5, 10))
        self.rect = self.image.get_rect()
        self.speed_ = 0
        self.rect.x = 450
        self.mask = pygame.mask.from_surface(self.scale_image)
        self.mask.scale((1, 1))
        self.radius = 40

    def move(self, x):
        self.speed_ += x

    def update(self):
        self.rect.y = SCREEN_HEIGHT - 100
        self.rect.x += self.speed_

        # Limitar al jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser_png.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.image_Scaled = pygame.transform.scale(self.image, (1, 1))
        self.mask.scale((1, 1))

    def update(self):
        self.rect.y -= 4

class AlienLaser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser_enemy.png").convert_alpha()
        self.scale_image = pygame.transform.scale(self.image, (1, 1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.scale_image)
        self.mask.scale((1, 1))
        self.radius = 5

    def update(self):
        self.rect.y += 4 

# -------------------------------game settings-------------------------------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
clock = pygame.time.Clock()
done = False
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
list_of_sprites = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
alien_laser_list = pygame.sprite.Group()
player_ = Player()
list_of_sprites.add(player_)



laser_list = pygame.sprite.Group()

def laser_shower():

    alien_ls = AlienLaser()
    alien_ls.rect.x = random.randrange(900)
    alien_laser_list.add(alien_ls)
    list_of_sprites.add(alien_ls)
    if alien_ls.rect.y > 600:
        pygame.sprite.Sprite.kill(alien_ls)

 # Ajusté la cantidad inicial de vidas

for x in range(20):
    enemy = Alien()
    enemy.rect.x = random.randrange(900 - 70)
    enemy.rect.y = random.randrange(SCREEN_HEIGHT - 200)
    enemy_list.add(enemy)
    list_of_sprites.add(enemy)

# run game
lives =3
score =0

def reset_game():
    global enemy_list
    global alien_laser_list
    alien_laser_list.empty()
    enemy_list.empty()  # Eliminar todos los enemigos actuales
    list_of_sprites.empty()
    list_of_sprites.add(player_)
    for y_ in range(20):
        enemy = Alien()
        enemy.rect.x = random.randrange(900 - 70)
        enemy.rect.y = random.randrange(SCREEN_HEIGHT - 200)
        enemy_list.add(enemy)
        list_of_sprites.add(enemy)


def next_level():
    global enemy_list
    global alien_laser_list
    alien_laser_list.empty()
    enemy_list.empty()  # Eliminar todos los enemigos actuales
    list_of_sprites.empty()
    list_of_sprites.add(player_)

    for y__ in range(20):
        enemy = Alien()
        enemy.rect.x = random.randrange(900 - 70)
        enemy.rect.y = random.randrange(SCREEN_HEIGHT - 200)
        enemy_list.add(enemy)
        list_of_sprites.add(enemy)

def game_over(screen_):
    pygame.mixer.music.load("game-over-arcade-6435.mp3")
    pygame.mixer.music.play()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type ==pygame.KEYDOWN:
                if event.key ==pygame.K_a:
                    player_.rect.x = 450
                    player_.speed_ = 0
                    reset_game()
                    return False
                
                if event.type ==pygame.KEYUP:
                    player_.speed_ = 0
                
        
        # Dibuja la pantalla de Game Over
        screen_.fill((0, 0, 0))
        font_game_over = pygame.font.SysFont("Arial", 24, bold=True)
        game_over_text = font_game_over.render(f"Game Over Press (a) to play again  Your scrore is {score}", True, (255, 255, 255))

        screen.blit(game_over_text, (150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        clock.tick(60)



while not done:
    laser_sound =pygame.mixer.Sound("blaster-2-81267.mp3")

    font = pygame.font.SysFont("Arial", 12, bold=True)
    score_marker = font.render(f"Score: {score}", True, (255, 255, 255))
    font_lives = pygame.font.SysFont("Arial", 12, bold=True)
    font_lives_render = font_lives.render(f"Lives: {lives}", True, (255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_.move(-3)
            if event.key == pygame.K_RIGHT:
                player_.move(3)
            if event.key == pygame.K_SPACE:
                laser_sound.play()
                LAS = Laser()
                LAS.rect.x = player_.rect.x - 8
                LAS.rect.y = player_.rect.y - 20
                laser_list.add(LAS)
                list_of_sprites.add(LAS)
                if LAS.rect.y < 0:
                    pygame.sprite.Sprite.kill(LAS)
                laser_shower()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_.move(3)
            if event.key == pygame.K_RIGHT:
                player_.move(-3)

    # Verificar colisiones entre enemigos y láseres
    hit_enemy = pygame.sprite.groupcollide(enemy_list, laser_list, True, True)
    hit_player = pygame.sprite.spritecollide(player_, alien_laser_list, True, pygame.sprite.collide_circle)

    if hit_enemy:
        laser_shower()
        score += 1
        enemy_list.remove(Alien)
        if len(enemy_list) == 0:
            pygame.display.flip()
            pygame.time.delay(2000)  # Retraso

            next_level()

    if hit_player:
        lives -= 1
        if lives == 0:
            game_over(screen)
            lives =3
            score =0




    # Actualizar sprites
    list_of_sprites.update()
    screen.fill([0, 0, 0])

    screen.blit(score_marker, (10, 10))
    screen.blit(font_lives_render, (10, 20))

    list_of_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)


