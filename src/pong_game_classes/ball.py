import pygame
import random
from math import sin
from enum import Enum

class PongBallDirection(Enum):
    DOWN = -1
    UP = 1
    LEFT = -1
    RIGHT = 1

class PongBall:

    def __init__(self, radius:float=25.0, max_speed_x:float=900.0, max_speed_y:float=180.0, max_deflect_angle:float=30.0):
        from pong_game_classes.game import PongGame
        
        self.radius: float = radius
        self.max_speed_x: float = max_speed_x
        self.max_speed_y: float = max_speed_y
        self.max_deflection_angle: float = max_deflect_angle

        self.game = PongGame() # reference to game singleton instance
        self.coordinates = pygame.Vector2(self.game.mid_screen_coordinate)
        self.x_direction = PongBallDirection.LEFT.value
        self.y_direction = PongBallDirection.UP.value
        self.current_pcnt_max_speed: float = 0.5
        self.angle: float = 0.0
        self.rect = pygame.draw.circle(surface=self.game.screen, color="white", center=self.coordinates, radius=self.radius)


    def check_and_bounce_at_rect_collision(self, rect_obj:pygame.Rect) -> None:
        """Handles ball reflections upon horizontal collisions with any rect object passed in."""
        if rect_obj.colliderect(self.rect):
            self._bounce_off_paddle(rect_obj)
    
    def check_and_bounce_at_horizontal_boundary_collision(self) -> None:
        """Handles ball reflections upon vertical collisions with the screen boundary (lower and upper)."""
        lower_screen_collision = self.coordinates.y >= self.game.screen.get_height() - self.rect.height
        upper_screen_collision = self.coordinates.y <= self.rect.height/2
        if (lower_screen_collision or upper_screen_collision): self.y_direction *= -1 # reverse direction trick

    def update_circle_rect(self):
        self.rect = pygame.draw.circle(surface=self.game.screen, color="white", center=self.coordinates, radius=self.radius)

    def reset(self):
        """Resets ball coordinates and directional fields to initial defaults."""
        self.coordinates = pygame.Vector2(self.game.mid_screen_coordinate)
        self.x_direction = random.choice([PongBallDirection.LEFT.value, PongBallDirection.RIGHT.value])
        self.y_direction = PongBallDirection.UP.value
        self.current_pcnt_max_speed: float = 0.5
        self.angle:float = 0.0

    def update_trajectory(self) -> None:
        """Updates ball trajectory, called every frame."""
        self.coordinates.x += self.x_direction * self.max_speed_x * self.current_pcnt_max_speed * self.game.dt
        self.coordinates.y += self.y_direction * self.max_speed_y * self.current_pcnt_max_speed * abs(sin(self.angle)) * self.game.dt

    def yield_trajectory_prediction_data(self) -> dict:
        return {
                "x_position": self.coordinates.x,
                "y_position": self.coordinates.y,
                "x_velocity": self.x_direction * self.max_speed_x * self.current_pcnt_max_speed,
                "y_velocity": self.y_direction * self.max_speed_y * self.current_pcnt_max_speed * abs(sin(self.angle)),
                "x_direction": self.x_direction,
                "y_direction": self.y_direction,
                "lower_reflection_bound": self.game.screen.get_height() - self.rect.height,
                "upper_reflection_bound": self.rect.height/2
            }

    def _bounce_off_paddle(self, rect_obj:pygame.Rect) -> None:
        """Internal method implementation for 'bounce off paddle' logic."""
        
        dist_from_paddle_center = ( 
            ( rect_obj.y - ( self.coordinates.y - (rect_obj.height * 0.5) ) ) / rect_obj.height 
        )
        normalized_dist_from_paddle_center = 2 * round(dist_from_paddle_center, 2)
        
        if (normalized_dist_from_paddle_center > 1): 
            normalized_dist_from_paddle_center = 1
        
        if (normalized_dist_from_paddle_center < -1):
            normalized_dist_from_paddle_center = -1
        
        if (normalized_dist_from_paddle_center < 0):
            self.y_direction = PongBallDirection.UP.value
        else:
            self.y_direction = PongBallDirection.DOWN.value
        
        self.angle = normalized_dist_from_paddle_center * self.max_deflection_angle
        self.x_direction *= -1 # reverse direction trick
        self.current_pcnt_max_speed = min( (self.current_pcnt_max_speed*1.05), 1.0) # increase ball speed pcnt each deflection up to max(1.0)
        
        if self.game._debug_game:
            print("left paddle collision detected")
            print(f"ball y-component relative to paddle: {self.coordinates.y - (rect_obj.height * 0.5)}")
            print(f"left paddle y-component: {rect_obj.y}")
            print(f"normalized dist from paddle center: {normalized_dist_from_paddle_center}") # bottom: -1, center: 0, top: 1
            print(f"ball deflection angle: {self.angle}")