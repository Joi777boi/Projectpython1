import pygame
import random
import os

pygame.init()

# Окно
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 24)

# Рекорд
HIGH_SCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Отрисовка текста
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# Меню
def menu():
    while True:
        screen.fill(BLACK)
        draw_text("SNAKE PRO", 230, 120)
        draw_text("Press ENTER to Start", 180, 180)
        draw_text("ESC to Quit", 220, 220)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Игра
def game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL, 0)

    food = (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

    score = 0
    speed = 10
    highscore = load_highscore()

    paused = False

    while True:
        screen.fill(BLACK)

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                if not paused:
                    if event.key == pygame.K_UP and direction != (0, CELL):
                        direction = (0, -CELL)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                        direction = (0, CELL)
                    elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                        direction = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        direction = (CELL, 0)

        if paused:
            draw_text("PAUSED", 260, 180)
            pygame.display.flip()
            continue

        # Движение
        head = (snake[0][0] + direction[0],
                snake[0][1] + direction[1])

        # Столкновения
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake):
            if score > highscore:
                save_highscore(score)
            return score

        snake.insert(0, head)

        # Еда
        if head == food:
            score += 1
            speed += 0.5  # ускорение
            food = (random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL))
        else:
            snake.pop()

        # Отрисовка
        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (*segment, CELL, CELL))

        pygame.draw.rect(screen, RED, (*food, CELL, CELL))

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"High: {highscore}", 10, 40)

        pygame.display.flip()
        clock.tick(speed)

# Экран проигрыша
def game_over(score):
    while True:
        screen.fill(BLACK)
        draw_text(f"GAME OVER", 230, 140)
        draw_text(f"Score: {score}", 240, 180)
        draw_text("Press R to Restart", 190, 220)
        draw_text("ESC to Menu", 210, 260)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

# Главный цикл
while True:
    menu()
    score = game()
    action = game_over(score)

    if action == "restart":
        continue
    
    
    