import pygame
import random
from entity import Shuttle, Alien
from projectile import Projectile

# Inizializzazione delle dimensioni della finestra di gioco
WIDTH = 700
HEIGHT = 700

# Inizializzazione dei colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inizializzazione delle velocità di gioco
SHUTTLE_SPEED = 8
PROJECTILE_SPEED = 8
ALIEN_SPEED = 5

# Inizializzazione dei proiettili e dei cooldown
shuttle_projectiles = []
alien_projectiles = []
COOLDOWN_SHUTTLE_SHOOT_TIME = 700  # in millisecondi
COOLDOWN_ALIEN_SHOOT_TIME = 1500  # in millisecondi
last_shuttle_shoot_time = 0
last_alien_shoot_time = 0

# Inizializzazione del punteggio
score = 0

# Inizializzazione di Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Caricamento degli oggetti Shuttle e Alien
shuttle = Shuttle(WIDTH, HEIGHT, "./PNGS/space-ship.png")
aliens = []  # Lista per memorizzare gli alieni

# Caricamento e settaggio della musica e dei sound
music = pygame.mixer.music.load("./sounds/Soundtrack.wav")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# Caricamento dei sound effect
shuttle_shoot_sound = pygame.mixer.Sound("./sounds/Shuttle Shootin.wav")

def create_shuttle_projectile():
    shuttle_projectiles.append(Projectile(shuttle.rect.centerx, shuttle.rect.top, "up"))

def create_alien_projectile(alien):
    alien_projectiles.append(Projectile(alien.rect.centerx, alien.rect.bottom, "down"))

def move_projectiles():
    for projectile in shuttle_projectiles:
        projectile.move(PROJECTILE_SPEED)
    for projectile in alien_projectiles:
        projectile.move(PROJECTILE_SPEED)

def draw_projectiles():
    for projectile in shuttle_projectiles:
        projectile.draw(screen, WHITE)
    for projectile in alien_projectiles:
        projectile.draw(screen, WHITE)

def create_aliens():
    alien_image_paths = ["./PNGS/alien.png", "./PNGS/alien.png", "./PNGS/alien.png"]  # Lista di percorsi delle immagini degli alieni
    alien_spacing = 100  # Spaziatura tra gli alieni
    num_aliens = 5  # Numero di alieni da creare

    for i in range(num_aliens):
        alien_image_path = random.choice(alien_image_paths)
        alien = Alien(WIDTH, HEIGHT, alien_image_path)
        alien.rect.centerx = (i + 1) * alien_spacing
        aliens.append(alien)

def check_collisions():
    global score

    # Controllo collisioni tra proiettili dello shuttle e alieni
    for projectile in shuttle_projectiles:
        for alien in aliens:
            if projectile.rect.colliderect(alien.rect):
                shuttle_projectiles.remove(projectile)
                aliens.remove(alien)
                score += 100

    # Controllo collisioni tra proiettili degli alieni e shuttle
    for projectile in alien_projectiles:
        if projectile.rect.colliderect(shuttle.rect):
            game_over()

def game_over():
    global running

    running = False
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2 + 50))
    pygame.display.flip()

def game_victory():
    global running

    running = False
    screen.fill(BLACK)
    victory_text = font.render("VICTORY!", True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2 + 50))
    pygame.display.flip()

# Creazione degli alieni
create_aliens()

# Ciclo principale del gioco
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento dello shuttle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and shuttle.rect.centerx >= 30:
        shuttle.move_left(SHUTTLE_SPEED)
    if keys[pygame.K_RIGHT] and shuttle.rect.centerx <= WIDTH - 30:
        shuttle.move_right(SHUTTLE_SPEED)
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shuttle_shoot_time >= COOLDOWN_SHUTTLE_SHOOT_TIME:
            create_shuttle_projectile()
            shuttle_shoot_sound.play()
            last_shuttle_shoot_time = current_time

    # Movimento degli alieni
    current_time = pygame.time.get_ticks()
    if current_time % 2000 == 0:
        for alien in aliens:
            if alien.rect.x <= 30 or alien.rect.x >= WIDTH - alien.rect.width - 30:
                alien.move_down(ALIEN_SPEED)
            else:
                if alien.rect.y % (2 * alien.rect.height) == 0:
                    alien.move_left(ALIEN_SPEED)
                else:
                    alien.move_right(ALIEN_SPEED)

    for alien in aliens:
        alien.update(ALIEN_SPEED)  # Aggiornamento del movimento degli alieni

    # Shooting degli alieni
    current_time = pygame.time.get_ticks()
    if current_time - last_alien_shoot_time >= COOLDOWN_ALIEN_SHOOT_TIME:
        alien_to_shoot = random.choice(aliens)
        create_alien_projectile(alien_to_shoot)
        last_alien_shoot_time = current_time

    # Pulizia dello schermo
    screen.fill(BLACK)

    # Disegno dello shuttle, degli alieni e dei proiettili 
    shuttle.draw(screen)  # Disegna lo shuttle
    for alien in aliens:
        alien.draw(screen)  # Disegna gli alieni
    draw_projectiles()  # Disegna i proiettili

    # Muovi i proiettili
    move_projectiles()

    # Controllo delle collisioni
    check_collisions()

    # Controllo vittoria
    if len(aliens) == 0:
        game_victory()

    # Aggiornamento dello schermo
    pygame.display.flip()
    clock.tick(60)

# Chiusura di pygame
pygame.quit()
