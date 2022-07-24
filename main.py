import pygame
from animate import happy_animate
import data
import random

pygame.init()
screen = pygame.display.set_mode((605, 780))

# set title, icon
pygame.display.set_caption("Sudoku Self-Solver")
icon = pygame.image.load('ai.png')
pygame.display.set_icon(icon)


clock = pygame.time.Clock()
gap = 55
fnt = pygame.font.SysFont("comicsans", 30)
grid2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def draw(grid):
    # draw existing numbers and rectangle color
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                img = fnt.render(str(grid[i][j]), True, (0, 0, 0))
                x1 = ((j+1) * gap)
                y1 = ((i+1) * gap)
                pygame.draw.rect(screen, (70, 163, 245), (x1, y1, gap, gap))
                screen.blit(img, (x1 + 18, y1 + 9))
                line()


def line():
    # draw sudoku grid line
    for i in range(1, 11):
        if (i-1) % 3 == 0 and i != 1 and i != 10:
            thick = 4
        else:
            thick = 1
        # draw horizon line
        pygame.draw.line(screen, (0, 0, 0), (gap, i * gap),
                         (gap * 10, i * gap), thick)

        # draw vertical line
        pygame.draw.line(screen, (0, 0, 0), (i * gap, gap),
                         (i * gap, gap * 10), thick)


def draw_highlight(grid, x, y, val):
    # draw highlight for the number
    position_x = ((y+1) * gap)
    position_y = ((x+1) * gap)
    pygame.draw.rect(screen, (224, 224, 224),
                     (position_x + 2, position_y + 2, 52, 52), 3)

    if val == 1:  # soft blue color / change by solving
        pygame.draw.rect(screen, (227, 241, 255),
                         (position_x, position_y, gap, gap))
    if val == 2:  # red color / back tracking
        pygame.draw.rect(screen, (255, 204, 209),
                         (position_x, position_y, gap, gap))
    if grid[x][y] != 0:
        img = fnt.render(str(grid[x][y]), True, (0, 0, 0))
        screen.blit(img, (position_x + 18, position_y + 9))
    line()


def final_draw(grid):
    # draw the solved number only (original excluded) grid2 is the input
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                position_x = ((j+1) * gap)
                position_y = ((i+1) * gap)
                img = fnt.render(str(grid[i][j]), True, (0, 0, 0))
                pygame.draw.rect(screen, (227, 241, 255),
                                 (position_x, position_y, gap, gap))
                screen.blit(img, (position_x + 18, position_y + 9))
                line()


def possible(grid, x, y, n):
    for i in range(9):
        if grid[x][i] == n and i != y:
            return False

    for i in range(0, 9):
        if grid[i][y] == n and i != x:
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):
            if grid[X][Y] == n:
                return False
    return True


def find_empty(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                return x, y
    return None, None


def solve(grid):
    row, col = find_empty(grid)
    if row is None:
        return True
    pygame.event.pump()
    for n in range(1, 10):
        if possible(grid, row, col, n):
            grid[row][col] = n
            grid2[row][col] = n
            draw_highlight(grid, row, col, 1)
            pygame.display.update()
            pygame.time.delay(12)

            if solve(grid):
                return True

        grid[row][col] = 0
        grid2[row][col] = 0
        draw_highlight(grid, row, col, 2)
        pygame.display.update()
        pygame.time.delay(12)

    return False


def happy(i):
    # animation of happy boy
    happy = happy_animate[i]
    screen.blit(happy, (100, 400))


class Button():
    def __init__(self, x, y, image, scale):
        w = image.get_width()
        h = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(w * scale), int(h * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        action = False
        # mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked position
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action


# import blue button <for generate new board>, red button <to start the AI solving>
newboard_img = pygame.image.load('images/newboard.png')
start_img = pygame.image.load('images/start.png')
newboard_button = Button(90, 575, newboard_img, 1)
start_button = Button(350, 575, start_img, 1)


def main():
    value = 0  # for the animation frame
    run = True
    result = 0
    i = 0
    grid = data.all_board[1]
    while run:
        screen.fill((255, 255, 255))
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if value == 80:
            value = 0

        if result == 1:
            happy(value)

        draw(grid)

        if newboard_button.draw():
            i = random.randint(0, 4)
            grid = data.all_board[i]
            result = 0

        if start_button.draw():
            if solve(grid):
                result = 1

        if result == 1:
            final_draw(grid2)
        pygame.display.update()
        value += 1


main()
