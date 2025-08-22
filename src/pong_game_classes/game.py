import pygame
from time import sleep

from misc.get_parent_dir import ROOT_DIR
from misc.singleton_decorator import singleton
from pong_game_classes.ai_controller import AIController
from pong_game_classes.ball import PongBall
from pong_game_classes.paddle import PongPaddle
from pong_game_classes.player import Player

@singleton
class PongGame:

    def __init__(self, screen_width:int=1280, screen_length:int=720, mode:str="ai", ai_difficulty:str="easy", enable_sounds:str="0"):
        pygame.init()

        self.ai_difficulty: str = ai_difficulty
        self.mode: str = mode
        self.enable_sounds: bool = bool(int(enable_sounds))
        self._debug_game: bool = False      # set to True to assert debug print statements
        self.has_user_started_game: bool = False
        self.quit_game: bool = False
        self.points_per_game: int = 3       # change this to set the value of match point
        self.dt: float = 0.0
        self._caption: str = "PY-PONG!"
        self._icon_path: str = str(ROOT_DIR) + "\\resources\\icons\\pong.jpg"
        self._paddle_hit_sound_filepath: str = str(ROOT_DIR) + "\\resources\\sounds\\paddle_hit.wav"
        self._score_point_sound_filepath: str = str(ROOT_DIR) + "\\resources\\sounds\\score_point.wav"
        self._wall_bounce_sound_filepath: str = str(ROOT_DIR) + "\\resources\\sounds\\wall_bounce.wav"
        self._game_soundtrack_filepath: str = str(ROOT_DIR) + "\\resources\\sounds\\8bit-music-for-game copy.mp3"

        self.screen = pygame.display.set_mode(size=(screen_width, screen_length))
        self.font = pygame.font.SysFont(name="Comic Sans MS", size=30)
        self.clock = pygame.time.Clock()
        self._icon = pygame.image.load(self._icon_path)
        
        pygame.display.set_caption(self._caption)
        pygame.display.set_icon(self._icon)

        self.mid_screen_coordinate: tuple = (self.screen.get_width()*0.5, self.screen.get_height()*0.5) # [0]: x-coordinate, [1]: y-coordinate


    def bound_paddle_in_screen_window(self, paddle_obj: PongPaddle):
        """Call this every frame to ensure the paddle cannot 'escape' the game window."""
        paddle_obj.rect.top = min(paddle_obj.rect.top, (self.screen.get_height() - paddle_obj.rect.height) )
        paddle_obj.rect.top = max(paddle_obj.rect.top, 0)
    
    def check_if_user_has_started_game(self) -> bool:
        """Returns True if the user has started the game, otherwise returns False."""
        if self.has_user_started_game:
            return True
        else:
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_SPACE]:
                self.has_user_started_game = True
            return self.has_user_started_game

    def check_if_user_quit(self) -> bool:
        """Returns True if the user attempts to close the game window, otherwise returns False."""
        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                #print("debug -")
                self.quit_game = True
            return self.quit_game

    def check_for_vertical_boundary_collision(
            self, ball_obj: PongBall, left_paddle_obj: PongPaddle, right_paddle_obj: PongPaddle, player_1_obj:Player, player_2_obj:Player
        ) -> None:
        """Checks for vertical boundary collision (out of bounds) and updates game state accordingly."""
        left_paddle_wins: bool = ball_obj.rect.x >= self.screen.get_width() - ball_obj.rect.width
        right_paddle_wins: bool = ball_obj.rect.x <= 0

        if (left_paddle_wins or right_paddle_wins):
            # somone wins (should set score appropriately and reset ball and paddles)
            if self.enable_sounds: self.play_score_point_sound()
            if left_paddle_wins:    
                player_1_obj.increment_score()
            else:
                player_2_obj.increment_score()
            ball_obj.reset()
            left_paddle_obj.reset()
            right_paddle_obj.reset()
            pygame.display.flip()
            
    def check_for_winner(self, player_1_obj:Player, player_2_obj:Player) -> None:
        """Checks for winner and updates game state accordingly."""
        players = (player_1_obj, player_2_obj)
        x_offsets = (0.6, 1.2)

        for idx, player in enumerate(players):
            if player.get_score() == self.points_per_game:
                player_1_obj.reset()
                player_2_obj.reset()
                self.set_screen_text(msg=f"{player.get_name()} WINS.", x_offset_mult=x_offsets[idx], y_offset_mult=1.35)
                self.has_user_started_game = False
                pygame.display.flip()
                if self.enable_sounds: self.play_game_soundtrack()
                sleep(3) # TODO: Try to figure out a better way to transition between games than just having this arbitrary delay.

    def close_and_cleanup(self) -> None:
        """Simply a wrapper around pygame.quit() for now, if additional cleanup clode is needed it should be included here."""
        pygame.quit()

    def debug_print_if_enabled(self, ball_obj: PongBall, left_paddle_obj: PongPaddle, right_paddle_obj: PongPaddle) -> None:
        """Debug print statements. Put near end of game loop. Only prints if self.debug is True"""
        if self._debug_game:
            pygame.draw.rect(surface=self.screen, color="red", rect=left_paddle_obj.rect, width=1)
            pygame.draw.rect(surface=self.screen, color="green", rect=ball_obj.rect, width=1)
            pygame.draw.rect(surface=self.screen, color="blue", rect=right_paddle_obj.rect, width=1)  

            print(f"left paddle coordinates: ({left_paddle_obj.rect.x}, {left_paddle_obj.rect.y})") 
            print(f"right paddle coordinates: ({right_paddle_obj.rect.x}, {right_paddle_obj.rect.y})") 
            print(f"ball coordinates: ({round(ball_obj.coordinates.x,2)}, {round(ball_obj.coordinates.y,2)})\n") 

    def draw_objects(self, ball_obj: PongBall, left_paddle_obj: PongPaddle, right_paddle_obj: PongPaddle) -> None:
        """This method is responsible for drawing all of the screen objects (exclusive of text) and is invoked every frame."""
        #pygame.draw.circle(surface=self.screen, color="white", center=ball_obj.coordinates, radius=ball_obj.radius)
        ball_obj.update_circle_rect()
        pygame.draw.rect(surface=self.screen, color=left_paddle_obj.color, rect=left_paddle_obj.rect)
        pygame.draw.rect(surface=self.screen, color=right_paddle_obj.color, rect=right_paddle_obj.rect)

        # vertical screen divide line
        pygame.draw.line(surface=self.screen, color="gray", start_pos=(self.mid_screen_coordinate[0], 0), end_pos=(self.mid_screen_coordinate[0], self.screen.get_height()))
        # top horizontal boundary line
        pygame.draw.line(surface=self.screen, color="gray", start_pos=(0, 0), end_pos=(self.screen.get_width(), 0), width=15) 
        # bottom horizontal boundary line
        pygame.draw.line(surface=self.screen, color="gray", start_pos=(0, self.screen.get_height()), end_pos=(self.screen.get_width(), self.screen.get_height()), width=15) 

    def end_frame(self) -> None: 
        """
            Ends the frame with displaying pending updates to the display and updating the dt for the game loop. 
            Put this at the very end of the game loop.
        """
        pygame.display.flip() # flip() the display to put your work on screen

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-independent physics
        self.dt = self.clock.tick(60) / 1000

    def make_move_for_ai(self, ball_obj: PongBall, right_paddle_obj: PongPaddle):
        # Need to get move from computer (either 'move_down', 'move_up', or 'stay' should be returned)
        computer_move: str = AIController.return_decision(
            ai_difficulty=self.ai_difficulty,
            ball_trajectory_snapshot=ball_obj.yield_trajectory_prediction_data(),
            paddle_position={"x": right_paddle_obj.rect.x, "y": right_paddle_obj.rect.y, "height": right_paddle_obj.paddle_height},
            game_dt=self.dt
        )
        if computer_move == "move_down": right_paddle_obj.move_down()
        elif computer_move == "move_up": right_paddle_obj.move_up()

    def map_user_key_press(self, left_paddle_obj: PongPaddle, right_paddle_obj: PongPaddle) -> None:
        """
            Scans for user keyboard presses and moves the paddles accordingly.
            Left paddle controls: 'a' moves the left paddle up, 's' moves the left paddle down.
            Right paddle controls (2-player mode only): 'up arrow' moves the right paddle up, 'down arrow' moves the right paddle down.
        """
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a]:
            left_paddle_obj.move_up()
        if keys_pressed[pygame.K_s]:
            left_paddle_obj.move_down()
        
        if self.mode == "2p":
            if keys_pressed[pygame.K_DOWN]:
                right_paddle_obj.move_down()
            if keys_pressed[pygame.K_UP]:
                right_paddle_obj.move_up()

    def play_sound(self, filepath:str):
        """Plays bounce sound effect once."""
        pygame.mixer.music.load(filename=filepath)
        pygame.mixer.music.play()

    def play_paddle_hit_sound(self):
        self.play_sound(filepath=self._paddle_hit_sound_filepath)

    def play_wall_bounce_sound(self):
        self.play_sound(filepath=self._wall_bounce_sound_filepath)

    def play_score_point_sound(self):
        self.play_sound(filepath=self._score_point_sound_filepath)

    def play_game_soundtrack(self):
        """Plays bounce sound effect in an infinite-loop."""
        pygame.mixer.music.load(filename=self._game_soundtrack_filepath)
        pygame.mixer.music.play(loops=-1)

    def return_rect(self, object_containing_rect):
        """Adapter that takes in an object containing a Pygame.Rect field and returns the Rect."""
        return object_containing_rect.rect

    def set_screen_text(self, msg:str, x_offset_mult:float, y_offset_mult:float) -> None:
        """Multipliers are to offset text coordinate to ideal location on screen 
            (referenced to center of the screen, e.g., x_offset_mult=1, y_offset_mult1 would center the text in the middle of the screen)
        """
        x: float = self.mid_screen_coordinate[0] * x_offset_mult
        y: float = self.mid_screen_coordinate[1] * y_offset_mult
        self.screen.blit(self.font.render(msg, False, "white"), dest=(x, y))