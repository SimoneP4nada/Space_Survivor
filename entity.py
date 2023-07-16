import pygame

class Shuttle:
    def __init__(self, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 30
        self.width = width

    def move_left(self, speed):
        self.rect.x -= speed
    
    def move_right(self, speed):
        self.rect.x += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Alien:
    def __init__(self, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = 40
        self.width = width
        self.direction = 1

    def move_left(self, speed):
        self.rect.x -= speed
        if self.rect.left <= 30:
            self.direction = 1  # Cambia direzione verso destra

    def move_right(self, speed):
        self.rect.x += speed
        if self.rect.right >= self.width - 30:
            self.direction = -1  # Cambia direzione verso sinistra

    def move_down(self, speed):
        self.rect.y += speed

    def update(self, speed):
        if self.direction == 1:
            self.move_right(speed)
            if self.rect.right >= self.width - 30:
                self.move_down(speed)
        else:
            self.move_left(speed)
            if self.rect.left <= 30:
                self.move_down(speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

