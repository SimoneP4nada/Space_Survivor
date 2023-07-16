import pygame

class Projectile:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.direction = direction

    def move(self, speed):
        if self.direction == "up":
            self.rect.y -= speed
        elif self.direction == "down":
            self.rect.y += speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

