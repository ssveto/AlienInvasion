import pygame

class Ship:
    # A class to manage the ship.

    def __init__(self, ai_game):
        # initialize the ship and set its starting position.
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Loading the ship image and getting its rect.
        self.image = pygame.image.load('/home/ssveto/Documents/python projects/alienInvasion/images/shipfinal.bmp')
        self.rect = self.image.get_rect()

        # storing a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Starting each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
    
    def update(self):
        # Update the ships position based on the movement flag.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # updating rect object from self.x
        
        self.x = float(self.rect.x)

    def blitme(self):
        # Drawing the ship at its current location.
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        # centering the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)