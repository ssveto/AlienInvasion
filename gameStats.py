class GameStats:
    # track statistics for Alien Invasion

    def __init__(self, ai_game):
        # initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()
        # starting AI in an active state
        self.game_active = False

    def reset_stats(self):
        # statistics that can change during the game
        self.ships_left = self.settings.ship_limit