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

    def __init__(self, radius:float=25.0, max_speed_x:float=500.0, max_speed_y:float=100.0, max_deflect_angle:float=30.0):
        from pong_game_classes.game import PongGame
        
        self.radius: float = radius
        self.max_speed_x: float = max_speed_x
        self.max_speed_y: float = max_speed_y
        self.max_deflection_angle: float = max_deflect_angle

        self.game = PongGame() # reference to game singleton instance
        self.coordinates = pygame.Vector2(self.game.mid_screen_coordinate)
        self.x_direction = PongBallDirection.LEFT.value
        self.y_direction = PongBallDirection.UP.value
        self.angle:float = 0.0
        self.rect = pygame.draw.circle(surface=self.game.screen, color="white", center=self.coordinates, radius=self.radius)


    def check_and_bounce_at_rect_collision(self, rect_obj:pygame.Rect) -> None:
        """Handles ball reflections upon horizontal collisions with any rect object passed in."""
        if rect_obj.colliderect(self.rect):
            self._bounce_off_paddle(rect_obj)
    
    def check_and_bounce_at_horizontal_boundary_collision(self) -> None:
        """Handles ball reflections upon vertical collisions with the screen boundary (upper and lower)."""
        upper_screen_collision = self.coordinates.y <= self.rect.height/2
        lower_screen_collision = self.coordinates.y >= self.game.screen.get_height() - self.rect.height
        if (upper_screen_collision or lower_screen_collision): self.y_direction *= -1 # reverse direction trick

    def update_circle_rect(self):
        self.rect = pygame.draw.circle(surface=self.game.screen, color="white", center=self.coordinates, radius=self.radius)

    def reset(self):
        """Resets ball coordinates and directional fields to initial defaults."""
        self.coordinates = pygame.Vector2(self.game.mid_screen_coordinate)
        self.x_direction = random.choice([PongBallDirection.LEFT.value, PongBallDirection.RIGHT.value])
        self.y_direction = PongBallDirection.UP.value
        self.angle:float = 0.0

    def update_trajectory(self) -> None:
        """Updates ball trajectory, called every frame."""
        self.coordinates.x += self.x_direction * self.max_speed_x * self.game.dt
        self.coordinates.y += self.y_direction * self.max_speed_y * abs(sin(self.angle)) * self.game.dt

    def _bounce_off_paddle(self, rect_obj:pygame.Rect) -> None:
        """Internal method implementation for 'bounce off paddle' logic."""
        #if self.game.debug_game:
        #    print("left paddle collision detected")
        #    print(f"ball y-component relative to paddle: {self.coordinates.y - (PADDLE_HEIGHT * 0.5)}")
        #    print(f"left paddle y-component: {paddle_rect.y}")
        
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
        
        if self.game._debug_game:
            print("left paddle collision detected")
            print(f"ball y-component relative to paddle: {self.coordinates.y - (rect_obj.height * 0.5)}")
            print(f"left paddle y-component: {rect_obj.y}")
            print(f"normalized dist from paddle center: {normalized_dist_from_paddle_center}") # bottom: -1, center: 0, top: 1
            print(f"ball deflection angle: {self.angle}")