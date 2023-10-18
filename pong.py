import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

sw = 800
sh = 600

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((sw, sh))
# set the window's title
pygame.display.set_caption('Pong')

# define game variables
live_ball = False
margin = 50
cpu_score = 0
player_score = 0
winner = 0
speed_increase = 0
ai_speed = 0

# define font
font = pygame.font.SysFont('Pixelify Sans', 40)

# define BG color
bg = (104, 0, 156)
white = (255, 255, 255)

# bg music
mixer.music.load('jerseyxclub.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)


def game_board():
    screen.fill(bg)
    # drawing a line boarder (where it starts and ends)
    # kinda like turtle
    pygame.draw.line(screen, white, (0, margin), (sw, margin))


def draw_text(text, font, text_color, x, y):
    # convert to image
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))


class paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 20, 100)
        self.speed = 5
        self.speed_x = -4
        self.speed_y = 4

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < sh:
            self.rect.move_ip(0, self.speed)

    def ai(self):
        # auto move paddle
        # move down
        if self.rect.centery < pong.rect.top and self.rect.bottom < sh:
            self.rect.move_ip(0, self.speed)

        # move up
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)


class ball:
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        # collision detection with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
        if self.rect.bottom > sh:
            self.speed_y *= -1

        # check collision with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
            ball_hit = mixer.Sound('pingponghit.mp3')
            mixer.Sound.set_volume(ball_hit, 0.5)
            ball_hit.play()

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > sw:
            self.winner = -1

        # update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 = player score, -1 = cpu score


# create paddles
player_paddle = paddle(sw - 40, sh // 2)
cpu_paddle = paddle(20, sh // 2)

# create pong ball
pong = ball(sw - 60, sh // 2 + 50)

while True:
    # prevents objects from moving as fast as the pc can run it
    fpsClock.tick(60)

    game_board()
    draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
    draw_text('P1: ' + str(player_score), font, white, sw - 90, 15)
    draw_text('BALL SPEED: ' + str(abs(pong.speed_x)), font, white, (sw // 2 - 100), 15)

    # draw paddles
    player_paddle.draw()
    cpu_paddle.draw()

    if live_ball:
        ai_speed += 1
        speed_increase += 1
        # move ball
        winner = pong.move()
        if winner == 0:
            # move paddle
            player_paddle.move()
            cpu_paddle.ai()
            # draw ball
            pong.draw()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1

    # print player instructions
    if live_ball == False:
        if winner == 0:
            draw_text('CLICK ANYWHERE TO START', font, white, 200, sh // 2 - 100)
        if winner == 1:
            draw_text('YOU SCORED!', font, white, sw // 2 - 100, sh // 2 - 100)
            draw_text('CLICK ANYWHERE TO RESTART', font, white, 190, sh // 2 - 50)
        if winner == -1:
            draw_text('CPU SCORED!', font, white, sw // 2 - 100, sh // 2 - 100)
            draw_text('CLICK ANYWHERE TO RESTART', font, white, 190, sh // 2 - 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            pong.reset(sw - 60, sh // 2 + 50)

    if speed_increase > 500:
        speed_increase = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1
        if pong.speed_x > 0:
            pong.speed_x += 1
        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1
    if ai_speed > 250:
        ai_speed = 0
        if cpu_paddle.speed < 0:
            cpu_paddle.speed -= -1
        if cpu_paddle.speed > 0:
            cpu_paddle.speed += 1
        if cpu_paddle.speed < 0:
            cpu_paddle.speed -= -1
        if cpu_paddle.speed > 0:
            cpu_paddle.speed += 1

    pygame.display.update()
