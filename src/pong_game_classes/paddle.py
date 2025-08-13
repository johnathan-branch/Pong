import pygame

from pong_game_classes.player import Player

PADDLE_LEFT_OFFSET: float = 0.025 # magic number to help with positioning of the paddle objects in the game loop
PADDLE_MAX_SPEED: float = 150.0

class PongPaddle:

    def __init__(self, player_assigned:Player, left_side_paddle:bool=True):
        from pong_game_classes.game import PongGame

        self.player_assigned = player_assigned

        self.game = PongGame() # reference to game singleton instance
        self.paddle_width: float = self.game.screen.get_width() * 0.025  # change this to change the width of the paddle
        self.paddle_height: float = self.game.screen.get_height() * 0.25 # change this to change the height of the paddle
        self.pos_top: float = self.game.mid_screen_coordinate[1] - (self.paddle_height  * 0.5) 

        if left_side_paddle:
            self.pos_left: float = self.game.screen.get_width() * PADDLE_LEFT_OFFSET                             
        else:
            self.pos_left: float = self.game.screen.get_width() * (1 - PADDLE_LEFT_OFFSET) - self.paddle_width                             
        
        self.rect = pygame.Rect(self.pos_left, self.pos_top, self.paddle_width, self.paddle_height)


    def move_up(self):
        self.rect.top -= PADDLE_MAX_SPEED * self.game.dt

    def move_down(self):
        self.rect.top += PADDLE_MAX_SPEED * self.game.dt

    def reset(self):
        """Resets paddle position to initial default."""
        self.pos_top = self.game.mid_screen_coordinate[1] - (self.paddle_height  * 0.5) 
        self.rect = pygame.Rect(self.pos_left, self.pos_top, self.paddle_width, self.paddle_height)