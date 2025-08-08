import pygame
from math import sin
from time import sleep

# pygame setup
pygame.init()
screen = pygame.display.set_mode(size=(1280, 720))
icon = pygame.image.load(f"resouces/icons/pong.jpg")
pygame.display.set_caption("PY-PONG!")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_loop_running: bool = True
has_user_started_game: bool = False
dt: float = 0.0
my_font = pygame.font.SysFont(name="Comic Sans MS", size=30)

# constants
DEBUG_GAME: bool = False
POINTS_PER_GAME: int = 5
MID_SCREEN_COORDINATE: tuple = (screen.get_width() * 0.5, screen.get_height() * 0.5) # [0]: x-coordinate, [1]:  y-coordinate
BALL_RADIUS: float = 25.0
BALL_MAX_SPEED_X: float = 500.0
BALL_MAX_SPEED_Y: float = BALL_MAX_SPEED_X / 5
BALL_MAX_DEFLECTION_ANGLE: int = 30
PADDLE_WIDTH: float = screen.get_width() * 0.025
PADDLE_HEIGHT: float = screen.get_height() * 0.25
PADDLE_LEFT_OFFSET: float = 0.025
PADDLE_TOP_OFFSET: float = 0.05
PADDLE_MAX_SPEED: float = 150.0

# game objects instantiations (ball, left_paddle, right_paddle)
ball_coordinates = pygame.Vector2(MID_SCREEN_COORDINATE)
ball_x_direction: int = -1
ball_y_direction: int = 1
ball_angle: float = 0.0

left_paddle_pos_left = screen.get_width() * PADDLE_LEFT_OFFSET
left_paddle_pos_top = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
left_paddle_rect = pygame.Rect(left_paddle_pos_left, left_paddle_pos_top, PADDLE_WIDTH, PADDLE_HEIGHT)
left_paddle_score: int = 0

right_paddle_pos_left: float = ( screen.get_width() * (1 - PADDLE_LEFT_OFFSET) ) - PADDLE_WIDTH
right_paddle_pos_top: float = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
right_paddle_rect = pygame.Rect(right_paddle_pos_left, right_paddle_pos_top, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle_score: int = 0

# game loop
while game_loop_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop_running = False

    screen.fill("black") # fill the screen with a color to wipe away anything from last frame

    if not has_user_started_game:
        # multipliers are magic numbers to offset text coordinate to ideal location on screen
        x: float = MID_SCREEN_COORDINATE[0] * 0.65 
        y: float = MID_SCREEN_COORDINATE[1] * 1.35
        screen.blit(my_font.render("Press SPACE to start the game.", False, "white"), dest=(x, y))

    ball_rect = pygame.draw.circle(surface=screen, color="white", center=ball_coordinates, radius=BALL_RADIUS)
    pygame.draw.rect(surface=screen, color="white", rect=left_paddle_rect)
    pygame.draw.rect(surface=screen, color="white", rect=right_paddle_rect)
    pygame.draw.line(surface=screen, color="gray", start_pos=(MID_SCREEN_COORDINATE[0],0), end_pos=(MID_SCREEN_COORDINATE[0],screen.get_height()))

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        has_user_started_game = True

    if has_user_started_game:
        
        if left_paddle_rect.colliderect(ball_rect):
            
            if DEBUG_GAME:
                print("left paddle collision detected")
                print(f"ball y-component relative to paddle: {ball_coordinates.y - (PADDLE_HEIGHT * 0.5)}")
                print(f"left paddle y-component: {left_paddle_rect.y}")
            
            dist_from_paddle_center = ( (left_paddle_rect.y - (ball_coordinates.y - (PADDLE_HEIGHT * 0.5))) / PADDLE_HEIGHT )
            normalized_dist_from_paddle_center = 2 * round(dist_from_paddle_center, 2)
            
            if (normalized_dist_from_paddle_center > 1): 
                normalized_dist_from_paddle_center = 1
            
            if (normalized_dist_from_paddle_center < -1):
                normalized_dist_from_paddle_center = -1
            
            if (normalized_dist_from_paddle_center < 0):
                ball_y_direction = 1
            else:
                ball_y_direction = -1
            
            ball_angle = normalized_dist_from_paddle_center * BALL_MAX_DEFLECTION_ANGLE
            ball_x_direction *= -1
            
            if DEBUG_GAME:
                print(f"normalized dist from paddle center: {normalized_dist_from_paddle_center}") # bottom: -1, center: 0, top: 1
                print(f"ball deflection angle: {ball_angle}")

        if right_paddle_rect.colliderect(ball_rect):
            
            if DEBUG_GAME:
                print("right paddle collision detected")
                print(f"ball y-component relative to paddle: {ball_coordinates.y - (PADDLE_HEIGHT * 0.5)}")
                print(f"right paddle y-component: {right_paddle_rect.y}")
            
            dist_from_paddle_center = ( (right_paddle_rect.y - (ball_coordinates.y - (PADDLE_HEIGHT * 0.5))) / PADDLE_HEIGHT )
            normalized_dist_from_paddle_center = 2 * round(dist_from_paddle_center, 2)
            
            if normalized_dist_from_paddle_center > 1: 
                normalized_dist_from_paddle_center = 1
            
            if normalized_dist_from_paddle_center < -1:
                normalized_dist_from_paddle_center = -1
            
            if normalized_dist_from_paddle_center < 0:
                ball_y_direction = 1
            else:
                ball_y_direction = -1
            
            ball_angle = normalized_dist_from_paddle_center * BALL_MAX_DEFLECTION_ANGLE
            ball_x_direction *= -1
            
            if DEBUG_GAME:
                print(f"normalized dist from paddle center: {normalized_dist_from_paddle_center}") # bottom: -1, center: 0, top: 1
                print(f"ball deflection angle: {ball_angle}")

        if (ball_coordinates.y <= ball_rect.height/2):
            # collision with top of the screen
            ball_y_direction *= -1

        if (ball_coordinates.y >= screen.get_height() - ball_rect.height):
            # collision with bottom of the screen
            ball_y_direction *= -1

        if (ball_coordinates.x <= 0):
            # right paddle wins (should set score and reset ball and paddles)
            right_paddle_score += 1
            ball_coordinates.x = MID_SCREEN_COORDINATE[0]
            ball_coordinates.y = MID_SCREEN_COORDINATE[1]
            ball_x_direction *= -1
            ball_y_direction = 1
            ball_angle = 0
            left_paddle_rect.top = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
            right_paddle_rect.top = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
            sleep(0.5)

        if (ball_coordinates.x >= screen.get_width() - ball_rect.width):
            left_paddle_score += 1
            # left paddle wins (should set score and reset ball and paddles)
            ball_coordinates.x = MID_SCREEN_COORDINATE[0]
            ball_coordinates.y = MID_SCREEN_COORDINATE[1]
            ball_x_direction *= -1
            ball_y_direction = 1
            ball_angle = 0
            left_paddle_rect.top = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
            right_paddle_rect.top = MID_SCREEN_COORDINATE[1] - (PADDLE_HEIGHT * 0.5)
            sleep(0.5)

        if keys_pressed[pygame.K_a]:
            left_paddle_rect.top += PADDLE_MAX_SPEED * dt
        if keys_pressed[pygame.K_s]:
            left_paddle_rect.top -= PADDLE_MAX_SPEED * dt
        if keys_pressed[pygame.K_DOWN]:
            right_paddle_rect.top += PADDLE_MAX_SPEED * dt
        if keys_pressed[pygame.K_UP]:
            right_paddle_rect.top -= PADDLE_MAX_SPEED * dt

        left_paddle_rect.top = min(left_paddle_rect.top, screen.get_height()-PADDLE_HEIGHT)
        left_paddle_rect.top = max(left_paddle_rect.top, 0)
        right_paddle_rect.top = min(right_paddle_rect.top, screen.get_height()-PADDLE_HEIGHT)
        right_paddle_rect.top  = max(right_paddle_rect.top , 0)
        ball_coordinates.x += ball_x_direction * BALL_MAX_SPEED_X * dt
        ball_coordinates.y += ball_y_direction * BALL_MAX_SPEED_Y * abs(sin(ball_angle)) * dt
        
        x = MID_SCREEN_COORDINATE[0] * 0.5 
        y = MID_SCREEN_COORDINATE[1] * 0.1 
        screen.blit(my_font.render("1P-  " + str(left_paddle_score), False, "white"), dest=(x, y))
        
        x = MID_SCREEN_COORDINATE[0] * 1.5 
        screen.blit(my_font.render("2P-  " + str(right_paddle_score), False, "white"), dest=(x, y))

        if left_paddle_score == POINTS_PER_GAME:
            left_paddle_score = 0
            right_paddle_score = 0
            x = MID_SCREEN_COORDINATE[0] * 0.6
            y = MID_SCREEN_COORDINATE[1] * 1.35
            screen.blit(my_font.render("PLAYER 1 WINS.", False, "white"), dest=(x, y))
            has_user_started_game = False
            pygame.display.flip()
            sleep(3)

        if right_paddle_score == POINTS_PER_GAME:
            left_paddle_score = 0
            right_paddle_score = 0
            x = MID_SCREEN_COORDINATE[0] * 1.2
            y = MID_SCREEN_COORDINATE[1] * 1.35
            screen.blit(my_font.render("PLAYER 2 WINS.", False, "white"), dest=(x, y))
            has_user_started_game = False
            pygame.display.flip() 
            sleep(3)

        if DEBUG_GAME:
            pygame.draw.rect(surface=screen, color="red", rect=left_paddle_rect, width=1)
            pygame.draw.rect(surface=screen, color="green", rect=ball_rect, width=1)
            pygame.draw.rect(surface=screen, color="blue", rect=right_paddle_rect, width=1)  
            print(f"left paddle coordinates: ({left_paddle_rect.x}, {left_paddle_rect.y})") 
            print(f"right paddle coordinates: ({right_paddle_rect.x}, {right_paddle_rect.y})") 
            print(f"ball coordinates: ({round(ball_coordinates.x,2)}, {round(ball_coordinates.y,2)})\n") 
            
    pygame.display.flip() # flip() the display to put your work on screen

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics
    dt = clock.tick(60) / 1000

pygame.quit()