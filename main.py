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
PROJECTILE_SPEED = 10
ALIEN_SPEED = 6

# Inizializzazione dei proiettili e dei cooldown
shuttle_projectiles = []
alien_projectiles = []
COOLDOWN_SHUTTLE_SHOOT_TIME = 800  # in millisecondi
COOLDOWN_ALIEN_SHOOT_TIME = 1000  # in millisecondi
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
nlnum = 0

# Caricamento e settaggio della musica e dei sound
music = pygame.mixer.music.load("./sounds/Soundtrack.wav")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# Caricamento dei sound effect
shuttle_shoot_sound = pygame.mixer.Sound("./sounds/Shuttle Shootin.wav")

# Limite massimo per la discesa degli alieni
MAX_ALIEN_DESCENT = HEIGHT // 2

def next_level():
    global nlnum
    nlnum = nlnum + 1
    create_aliens()  # Creiamo nuovi alieni per il livello successivo

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
    global aliens  # Aggiungiamo questa linea per modificare la variabile globale
    alien_image_paths = ["./PNGS/alien.png", "./PNGS/alien.png", "./PNGS/alien.png"]  # Lista di percorsi delle immagini degli alieni
    alien_spacing_x = 100  # Spaziatura orizzontale tra gli alieni
    alien_spacing_y = 80  # Spaziatura verticale tra gli alieni
    num_aliens = 5 + nlnum  # Numero di alieni da creare

    aliens = []  # Reset degli alieni

    num_columns = WIDTH // alien_spacing_x  # Numero di colonne disponibili
    num_rows = (num_aliens // num_columns) + 1  # Numero di righe necessarie

    for row in range(num_rows):
        for col in range(num_columns):
            if len(aliens) < num_aliens:
                alien_image_path = random.choice(alien_image_paths)
                alien = Alien(WIDTH, HEIGHT, alien_image_path)
                alien.rect.centerx = (col + 1) * alien_spacing_x
                alien.rect.centery = (row + 1) * alien_spacing_y
                aliens.append(alien)

def check_collisions():
    global score

    # Liste temporanee per memorizzare i proiettili e gli alieni da rimuovere
    shuttle_projectiles_to_remove = []
    aliens_to_remove = []
    alien_projectiles_to_remove = []

    # Controllo collisioni tra proiettili dello shuttle e alieni
    for projectile in shuttle_projectiles:
        for alien in aliens:
            if projectile.rect.colliderect(alien.rect):
                shuttle_projectiles_to_remove.append(projectile)
                aliens_to_remove.append(alien)
                score += 100

    # Controllo collisioni tra proiettili degli alieni e shuttle
    for projectile in alien_projectiles:
        if projectile.rect.colliderect(shuttle.rect):
            alien_projectiles_to_remove.append(projectile)
            game_over()

    # Rimozione dei proiettili e degli alieni dopo aver controllato tutte le collisioni
    for projectile in shuttle_projectiles_to_remove:
        if projectile in shuttle_projectiles:
            shuttle_projectiles.remove(projectile)
    for alien in aliens_to_remove:
        if alien in aliens:
            aliens.remove(alien)
    for projectile in alien_projectiles_to_remove:
        if projectile in alien_projectiles:
            alien_projectiles.remove(projectile)


def score_ingame():
    global score
    global running
    
    score_ingame_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_ingame_text, (WIDTH - 120, 20))
    pygame.display.flip()
      
      
def game_over():
    global running

    running = False
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER. Press SPACE to try again", True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2 + 50))
    pygame.display.flip()

# Creazione degli alieni
create_aliens()

# Loop esterno del gioco
while True:
    # Loop del gioco
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
                    if alien.rect.y + ALIEN_SPEED + 4 <= MAX_ALIEN_DESCENT:
                        alien.move_down(ALIEN_SPEED + 4)
                else:
                    if alien.rect.y % (2 * alien.rect.height) == 0:
                        if alien.rect.y + ALIEN_SPEED <= MAX_ALIEN_DESCENT:
                            alien.move_left(ALIEN_SPEED)
                    else:
                        if alien.rect.y + ALIEN_SPEED <= MAX_ALIEN_DESCENT:
                            alien.move_right(ALIEN_SPEED)

        for alien in aliens:
            if alien.rect.y + ALIEN_SPEED <= MAX_ALIEN_DESCENT:
                alien.update(ALIEN_SPEED)  # Aggiornamento del movimento degli alieni

        # Shooting degli alieni
        current_time = pygame.time.get_ticks()
        if current_time - last_alien_shoot_time >= COOLDOWN_ALIEN_SHOOT_TIME:
            if aliens:  # Verifichiamo che la lista non sia vuota
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
            next_level()
        
        #visualizzazione punteggio in-game    
        score_ingame()
        
        # Aggiornamento dello schermo
        pygame.display.flip()
        clock.tick(60)

    # Schermata di game over 
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                score = 0
                shuttle_projectiles = []
                alien_projectiles = []
                aliens = []
                create_aliens()  # Ricrea gli alieni per il nuovo gioco
