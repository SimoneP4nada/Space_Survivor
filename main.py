import pygame
import random

# Inizializzazione delle dimensioni della finestra di gioco
WIDTH = 700
HEIGHT = 700

# Inizializzazione dei colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inizializzazione delle velocità di gioco
SHUTTLE_SPEED = 8
PROJECTILE_SPEED = 8

# Inizializzazione delle dimensioni dello shuttle
SHUTTLE_WIDTH = 32
SHUTTLE_HEIGHT = 32

# Inizializzazione delle coordinate di partenza dello shuttle
shuttle_X = (WIDTH - SHUTTLE_WIDTH) // 2

# Inizializzazione sprite shuttle
shuttle = pygame.image.load("./PNGS/space-ship.png")
shuttle_rect = shuttle.get_rect()
shuttle_rect.centerx = shuttle_X
shuttle_rect.bottom = HEIGHT - 30

# Inizializzazione dei punteggi dei giocatori
player_score = 0

# Inizializzazione dei proiettili e dei cooldown
projectiles = []
COOLDOWN_SHOOT_TIME = 500  # in millisecondi
# Variabile per memorizzare l'ultimo tempo dello sparo
last_shoot_time = 0

# Inizializzazione di pygame
pygame.init()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Funzione per disegnare lo shuttle
def draw_shuttle():
    screen.blit(shuttle, shuttle_rect)

# Funzione per disegnare i proiettili
def draw_projectiles():
    for projectile in projectiles:
        pygame.draw.circle(screen, WHITE, (projectile[0], projectile[1]), 5)

# Funzione per muovere i proiettili verso l'alto
def move_projectiles():
    for i in range(len(projectiles)):
        projectiles[i] = (projectiles[i][0], projectiles[i][1] - PROJECTILE_SPEED)

# Ciclo principale del gioco
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento dello shuttle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shuttle_rect.x -= SHUTTLE_SPEED
        if shuttle_rect.right < 0:  # Se lo shuttle esce dal lato sinistro dello schermo
            shuttle_rect.left = WIDTH  # Riporta lo shuttle al lato destro dello schermo

    if keys[pygame.K_RIGHT]:
        shuttle_rect.x += SHUTTLE_SPEED
        if shuttle_rect.left > WIDTH:  # Se lo shuttle esce dal lato destro dello schermo
            shuttle_rect.right = 0  # Riporta lo shuttle al lato sinistro dello schermo

    # Comandi dello Shuttle
    current_time = pygame.time.get_ticks()
    if current_time - last_shoot_time >= COOLDOWN_SHOOT_TIME:
        if keys[pygame.K_SPACE]:
            projectiles.append((shuttle_rect.centerx, shuttle_rect.top))
            last_shoot_time = current_time

    # Pulizia dello schermo
    screen.fill(BLACK)

    # Disegno dello shuttle e dei proiettili
    draw_shuttle()
    draw_projectiles()

    # Muovi i proiettili verso l'alto
    move_projectiles()

    # Aggiornamento dello schermo
    pygame.display.flip()
    clock.tick(60)

# Chiusura di pygame
pygame.quit()




