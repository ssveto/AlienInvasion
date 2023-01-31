import sys
import pygame
from time import sleep

from settings import Settings
from gameStats import GameStats
from ship import Ship
from bullet import Bullet
from button import Button
from alien import Alien


class AlienInvasion:
    # Overall class to manage game assets and behaviour
    def __init__(self):
        # Initialize the game, and create game resources.
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # an instance to store game statistics
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # making the play button
        self.play_button = Button(self, "Play")


    def run_game(self):
        # Starting the main loop for the game.
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()          
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            
            
           
            
                  



    def _check_events(self):
        # Responding to keypresses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        # start a new game when the player clicks play
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True

    def _check_keydown_events(self, event):
        # Responding to keypresses
        if event.key == pygame.K_RIGHT:
            # move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        #responding to key releases.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _create_fleet(self):
        # creating the fleet of aliens
        # finding number of aliens in a row and making space between them
    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (3 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # determining the number of rows of aliens that fit on the screen
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # create an alien and place it in the row
                self._create_alien(alien_number, row_number)
           
            
    
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_bullets(self):
        # Update position of bullets and get rid of old bullets
        #update bullet position
        self.bullets.update()
        # get rid of bullets that have dissappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        # check for bullets and hits, and get rid of bullets and aliens
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        # bullet alien collision
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) 
        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        # updating the possitions of all aliens in the fleet and check if the fleet is at an edge
        self._check_fleet_edges()

        self.aliens.update()
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # checking if aliens have hit the bottom of the screen
        self._check_aliens_bottom()
        
    def _check_fleet_edges(self):
        # responding if any aliens have reachend an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        # droping the entire fleet and changing its direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    

    def _ship_hit(self):
        # respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # creating a new fleet and centering the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        # check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        # Updates images on the screen, and flip to the new screen.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()


        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Making a game instance, and running the game.
    ai = AlienInvasion()
    ai.run_game()

