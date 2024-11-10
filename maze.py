import pygame
import random
import sys

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))]
    maze[stack[0][0]][stack[0][1]] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 1:
                neighbors.append((dx, dy))

        if neighbors:
            dx, dy = random.choice(neighbors)
            maze[x + dx][y + dy] = 0
            maze[x + dx * 2][y + dy * 2] = 0
            stack.append((x + dx * 2, y + dy * 2))
        else:
            stack.pop()

    return maze

class Player:
    def __init__(self):
        self.x, self.y = 1, 1

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y

def draw(maze, player, end_pos):
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.draw.rect(screen, BLUE, (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end_pos[0] * CELL_SIZE, end_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_instructions():
    font = pygame.font.Font(None, 36)
    instructions = [
        "Maze Game Instructions",
        "Use the arrow keys to navigate through the maze.",
        "Reach the red square to win!",
        "Press any key to start."
    ]
    screen.fill(WHITE)
    for i, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + i * 40))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_win_message():
    font = pygame.font.Font(None, 72)
    text = font.render("YOU WIN!", True, GREEN)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    maze = generate_maze()
    player = Player()
    end_pos = (COLS - 2, ROWS - 2)

    show_instructions()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, maze)
        if keys[pygame.K_UP]:
            player.move(0, -1, maze)
        if keys[pygame.K_DOWN]:
            player.move(0, 1, maze)

        draw(maze, player, end_pos)
        pygame.display.flip()

        if (player.x, player.y) == end_pos:
            show_win_message()
            main()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
