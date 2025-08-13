import pygame

from pong_game_classes.game import PongGame
from pong_game_classes.ball import PongBall
from pong_game_classes.paddle import PongPaddle
from pong_game_classes.player import Player

class GameLoop:

    def __init__(self):
    
        # game objects instantiations (game, players, left_paddle, right_paddle, and ball)
        self.game_instance = PongGame()

        self.player_1 = Player(name="P1- ")
        self.player_2 = Player(name="P2- ")
        self.left_paddle = PongPaddle(player_assigned=self.player_1)
        self.right_paddle = PongPaddle(player_assigned=self.player_2, left_side_paddle=False)
        self.ball = PongBall()

    def start(self):
        # game loop

        while not self.game_instance.quit_game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_instance.quit_game = True

            self.game_instance.screen.fill("black") # fill the screen with a color to wipe away anything from last frame
            self.game_instance.draw_objects(ball_obj=self.ball, left_paddle_obj=self.left_paddle, right_paddle_obj=self.right_paddle)

            if not self.game_instance.check_if_user_has_started_game():
                self.game_instance.set_screen_text(msg="Press SPACE to start the game.", x_offset_mult=0.65, y_offset_mult=1.35)

            else: 
                self.ball.check_and_bounce_at_rect_collision(rect_obj=self.game_instance.return_rect(self.left_paddle))
                self.ball.check_and_bounce_at_rect_collision(rect_obj=self.game_instance.return_rect(self.right_paddle))
                self.ball.check_and_bounce_at_horizontal_boundary_collision()
                self.ball.update_trajectory()

                self.game_instance.check_for_vertical_boundary_collision(
                    ball_obj=self.ball, 
                    left_paddle_obj=self.left_paddle, right_paddle_obj=self.right_paddle, 
                    player_1_obj=self.player_1, player_2_obj=self.player_2
                )
                self.game_instance.map_user_key_press(left_paddle_obj=self.left_paddle, right_paddle_obj=self.right_paddle)
                self.game_instance.bound_paddle_in_screen_window(paddle_obj=self.left_paddle)
                self.game_instance.bound_paddle_in_screen_window(paddle_obj=self.right_paddle)

                self.game_instance.set_screen_text(msg="1P-  " + str(self.player_1.get_score()), x_offset_mult=0.5, y_offset_mult=0.1)
                self.game_instance.set_screen_text(msg="2P-  " + str(self.player_2.get_score()), x_offset_mult=1.5, y_offset_mult=0.1)
                self.game_instance.check_for_winner(player_1_obj=self.player_1, player_2_obj=self.player_2)
                self.game_instance.debug_print_if_enabled(ball_obj=self.ball, left_paddle_obj=self.left_paddle, right_paddle_obj=self.right_paddle) # Only prints if game_instance._debug_game is True
            self.game_instance.end_frame() # MAKE SURE TO KEEP THIS AS THE LAST STATEMENT AT THE END OF THE GAME LOOP!

        self.game_instance.close_and_cleanup()