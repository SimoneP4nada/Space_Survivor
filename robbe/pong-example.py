import pygame
import random

# Inizializzazione delle dimensioni della finestra di gioco
WIDTH = 800
HEIGHT = 400

# Inizializzazione dei colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inizializzazione delle dimensioni dei paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# Inizializzazione delle velocità di gioco
PADDLE_SPEED = 5
BALL_X_SPEED = 3
BALL_Y_SPEED = 3

# Inizializzazione delle coordinate di partenza dei paddle e della palla
player_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
opponent_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# Inizializzazione delle direzioni della palla
ball_x_direction = random.choice([-1, 1])
ball_y_direction = random.choice([-1, 1])

# Inizializzazione dei punteggi dei giocatori
player_score = 0
opponent_score = 0

# Inizializzazione di pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Funzione per disegnare i paddle
def draw_paddle(paddle_x, paddle_y):
    pygame.draw.rect(screen, WHITE, pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Funzione per disegnare la palla
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), 5)

# Funzione per disegnare i punteggi
def draw_scores():
    player_text = font.render("Player: " + str(player_score), True, WHITE)
    opponent_text = font.render("Opponent: " + str(opponent_score), True, WHITE)
    screen.blit(player_text, (10, 10))
    screen.blit(opponent_text, (WIDTH - opponent_text.get_width() - 10, 10))

# Ciclo principale del gioco
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento del paddle del giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle_y > 0:
        player_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle_y < HEIGHT - PADDLE_HEIGHT:
        player_paddle_y += PADDLE_SPEED

    # Movimento del paddle dell'avversario
    if opponent_paddle_y < ball_y and opponent_paddle_y < HEIGHT - PADDLE_HEIGHT:
        opponent_paddle_y += PADDLE_SPEED
    if opponent_paddle_y > ball_y and opponent_paddle_y > 0:
        opponent_paddle_y -= PADDLE_SPEED

    # Movimento della palla
    ball_x += ball_x_direction * BALL_X_SPEED
    ball_y += ball_y_direction * BALL_Y_SPEED

    # Controllo delle collisioni con i paddle
    if ball_x <= PADDLE_WIDTH and player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT:
        ball_x_direction = 1
    if ball_x >= WIDTH - PADDLE_WIDTH and opponent_paddle_y <= ball_y <= opponent_paddle_y + PADDLE_HEIGHT:
        ball_x_direction = -1
    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_y_direction *= -1

    # Controllo dei punti segnati
    if ball_x < 0:
        opponent_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_x_direction = random.choice([-1, 1])
        ball_y_direction = random.choice([-1, 1])
    elif ball_x > WIDTH:
        player_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_x_direction = random.choice([-1, 1])
        ball_y_direction = random.choice([-1, 1])

    # Pulizia dello schermo
    screen.fill(BLACK)

    # Disegno dei paddle, della palla e dei punteggi
    draw_paddle(0, player_paddle_y)
    draw_paddle(WIDTH - PADDLE_WIDTH, opponent_paddle_y)
    draw_ball(ball_x, ball_y)
    draw_scores()

    # Aggiornamento dello schermo
    pygame.display.flip()
    clock.tick(60)

# Chiusura di pygame
pygame.quit()
