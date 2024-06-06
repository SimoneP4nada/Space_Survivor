import pygame
import random

# Inizializzazione delle dimensioni della finestra di gioco
WIDTH = 700
HEIGHT = 700

# Inizializzazione dei colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inizializzazione delle velocità di gioco
SHUTTLE_SPEED = 5
PROJECTILE_SPEED = 6

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

# Inizializzazione dei proiettili
projectiles = []

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
        pygame.draw.circle(screen, WHITE, (projectile[0], projectile[1]), 15)

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
    if keys[pygame.K_LEFT] and shuttle_rect.left > 20:
        shuttle_rect.x -= SHUTTLE_SPEED
    if keys[pygame.K_RIGHT] and shuttle_rect.right < (WIDTH-20):
        shuttle_rect.x += SHUTTLE_SPEED

    # Comandi dello Shuttle
    if keys[pygame.K_SPACE]:
        projectiles.append((shuttle_rect.centerx, shuttle_rect.top))

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
