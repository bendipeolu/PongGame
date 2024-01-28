import pygame
pygame.init()

WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

FONT = pygame.font.SysFont('comicsans', 30)
WHITE = (255, 255, 255)


# CLASSES

class Paddle:
    COLOR = WHITE
    VEL = 4
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, left=False, right=False):
        if left:
            self.x -= self.VEL
        else:
            self.x += self.VEL


class Ball:

    MAX_VEL = 3

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 0
        self.y_vel = self.MAX_VEL

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
            self.x += self.x_vel
            self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = 0

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 20

    def draw(self, win):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))



# FUNCTIONS 

def draw(win, paddle, ball, bricks, score, lives): 
    win.fill((0, 0, 0))

    score_text = FONT.render(f"Score: {score}", 1, (200, 55, 25))
    win.blit(score_text, (10, 10))

    lives_text = FONT.render(f"Lives: {lives}", 1, (25, 255, 55))
    win.blit(lives_text, (WIDTH - 120, 10))


    paddle.draw(win)
    ball.draw(win)

    for brick in bricks:
        brick.draw(win)

    pygame.display.update()


def handle_paddle_movement(keys, paddle):
    if keys[pygame.K_a] or keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
        paddle.move(left=True, right=False)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT] and paddle.x + paddle.VEL + paddle.width <= WIDTH:
        paddle.move(left=False, right=True)

def handle_collision(ball, paddle, bricks, score):

    # FOR SIDES OF SCREEN 
    if ball.x + ball.radius >= WIDTH or ball.x - ball.radius <= 0:
        ball.x_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # FOR HITTING PADDLE
    if ball.y_vel > 0:
        if ball.y + ball.radius >= paddle.y and ball.x + ball.radius >= paddle.x and ball.x - ball.radius <= paddle.x + paddle.width:
            ball.y_vel *= -1

            # DIRECTION OF BALL AFTER COLLISION
            middle_x = (paddle.x + paddle.width) / 2
            difference_in_x = middle_x - ball.x
            reduction_factor = (paddle.width / 2) / ball.MAX_VEL
            x_vel = difference_in_x / reduction_factor
            ball.x_vel = -1 * x_vel
        
    # COLLISON WITH BRICKS
    for brick in bricks:
        if ball.y - ball.radius <= brick.y + brick.height and ball.y + ball.radius >= brick.y:
            if ball.x + ball.radius >= brick.x and ball.x - ball.radius <= brick.x + brick.width:
                ball.y_vel *= -1
                bricks.remove(brick)
                score += 1
            elif ball.x - ball.radius <= brick.x + brick.width and ball.x + ball.radius >= brick.x:
                ball.y_vel *= -1
                bricks.remove(brick)
                score += 1
    
    return score

def create_bricks():
    bricks = []

    x = 5
    y = 50

    for row in range(8):
        for col in range(10):
            brick = Brick(x, y)
            bricks.append(brick)
            x += brick.width + 5
        x = 5
        y += brick.height + 5

    return bricks

bricks = create_bricks()


# ENDPOINTS
def game_over_screen(score, win):
    win.fill((0, 0, 0))

    game_over_text = FONT.render("Game Over", 1, (255, 0, 0))
    score_text = FONT.render(f"Final Score: {score}", 1, (255, 255, 255))

    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()

    # DISPLAY SCREEN FOR 3 SECONDS
    start_time = pygame.time.get_ticks()
    delay = 3000  

    while pygame.time.get_ticks() - start_time < delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()

def winning_screen(win):
    win.fill((0, 0, 0))

    game_over_text = FONT.render("YOU WIN!", 1, (255, 0, 0))

    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))


    pygame.display.update()
    start_time = pygame.time.get_ticks()
    delay = 3000  # Delay in milliseconds (3 seconds)

    while pygame.time.get_ticks() - start_time < delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()


    

def main():
    run = True
    clock = pygame.time.Clock()

    paddle = Paddle(200, 660, 100, 20)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7)

    score = 0
    lives = 5

    time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)

        if time % 2000 == 0:
            ball.radius = ball.radius / 5

        draw(WIN, paddle, ball, bricks, score, lives)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, paddle)

        ball.move()
        score = handle_collision(ball, paddle, bricks, score)

        if ball.y > HEIGHT:
            lives -= 1
            ball.reset()


        if lives == 0:
            game_over_screen(score, WIN)
            run = False
        
        if len(bricks) == 0:
            winning_screen(WIN)
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()

