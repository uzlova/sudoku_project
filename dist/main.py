# The music I used:
# https://fallenblood.itch.io/50-sfx
# https://retroindiejosh.itch.io/free-music-pack-14-lo-fi-chill
# https://joshuuu.itch.io/short-loopable-background-music


import os
import sys

import pygame
from pygame.examples.aliens import load_image

from board import Board
from sudoky_solution import SudokuSolver

pygame.init()


# _____________________________________________ИЗ TXT ВО ВЛОЖЕНННЫЙ СПИСОК__________________________________________ #
def read_sudoku(filename):
    matrix = []

    s = []
    with open(f"sudoku_options/{filename}") as f:
        for line in f:
            for item in line:
                if len(s) == 9:
                    matrix.extend([s])
                    s = []

                if item == '.':
                    s.append('.')
                if item.isdigit():
                    s.append(int(item))

        if len(s) == 9:
            matrix.extend([s])

    return matrix


# _____________________________________________________CONST_________________________________________________________ #
LEVELS = os.listdir('sudoku_options') * 3
n = 0

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 15
SIZE_TILE = 50
COLORS = {
    0: (255, 255, 255),  # WHITE
    1: (0, 0, 0),  # BLACK
    3: (238, 122, 147),  # LIGHT PINK
    4: (255, 24, 124),  # DARK PINK
    5: (255, 228, 225),  # MISTY ROSE
    6: (34, 34, 34),  # DARK GREY

    7: (225, 243, 255),  # LIGHT BLUE
    8: (109, 208, 230),  # BLUE
    9: (24, 77, 255)  # Bright blue
}

FONT_1 = pygame.font.Font('venv/fonts/Montserrat-Bold.ttf', 22)
FONT_2 = pygame.font.Font('venv/fonts/Montserrat-Bold.ttf', 36)  # ДЛЯ КЛЕТОК СУДОКУ
FONT_3 = pygame.font.Font('venv/fonts/Montserrat-Bold.ttf', 16)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sound_click_1 = pygame.mixer.Sound('Select_007.wav')
sound_click_2 = pygame.mixer.Sound('Select_001.wav')
sound_click_2.set_volume(0.3)
sound_click_1.set_volume(0.2)

pygame.mixer.music.load('star-reaction.ogg')
pygame.mixer.music.play()

clock = pygame.time.Clock()
pygame.display.set_caption('Судоку')


# ____________________________________________________ГИФ АНИМАЦИЯ__________________________________________________ #
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
        self.images = [pygame.image.load('1.png'), pygame.image.load('2.png'),
                       pygame.image.load('3.png'), pygame.image.load('4.png'),
                       pygame.image.load('5.png'), pygame.image.load('6.png'),
                       pygame.image.load('7.png'), pygame.image.load('8.png'),
                       pygame.image.load('9.png'), pygame.image.load('10.png'),
                       pygame.image.load('11.png'), pygame.image.load('12.png')]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


# __________________________________________________КЛАСС СУДОКУ___________________________________________________#
class Sudoku(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.cell_size = SIZE_TILE
        self.cell_size_2 = SIZE_TILE * 3
        self.win = False
        self.BOARD = read_sudoku(LEVELS[n])
        self.SOLUTION = SudokuSolver.solve(self.BOARD)
        self.lose = False

    def terminate(self):
        pygame.quit()
        sys.exit()

    def check_cells(self, screen):
        self.blocked_cells = {}  # координаты клетки, числа в которых нельзя поменять
        self.open_cells = {}  # клетки(rect), открытые для изменений
        for y in range(self.height):
            for x in range(self.width):
                if self.BOARD[y][x] != '.':  # сверяемся с матрицей BOARD
                    self.blocked_cells[(x * self.cell_size + self.left, y * self.cell_size)] = str(self.BOARD[y][x])
                if self.BOARD[y][x] == '.':
                    self.open_cells[(x, y)] = (x * self.cell_size + self.left, y * self.cell_size)
        return self.open_cells

    def render(self, screen):
        n = 0

        for i in self.BOARD:
            q = i.count('.')
            n += q
        if n == 0:
            if self.BOARD == self.SOLUTION:
                self.win = True
            else:
                self.lose = True
        for y in range(self.height):
            for x in range(self.width):
                if self.BOARD[y][x] != '.' and (x, y) not in self.open_cells.keys():  # сверяемся с матрицей BOARD
                    color_1 = COLORS[5]
                    color_2 = COLORS[3]

                elif self.BOARD[y][x] != '.' and (x, y) in self.open_cells.keys():
                    color_1 = COLORS[7]
                    color_2 = COLORS[8]

                else:
                    color_1 = COLORS[5]
                    color_2 = COLORS[3]

                pygame.draw.rect(screen, color_1, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                                   self.cell_size,
                                                   self.cell_size), 0)
                pygame.draw.rect(screen, color_2, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                                   self.cell_size,
                                                   self.cell_size), 2)
        for y in range(3):
            for x in range(3):
                pygame.draw.rect(screen, COLORS[4],
                                 (x * self.cell_size_2 + self.left, y * self.cell_size_2 + self.top,
                                  self.cell_size_2, self.cell_size_2), 2)
        for key in self.blocked_cells:
            text = FONT_2.render(self.blocked_cells[key], True, COLORS[4])
            x, y = key
            screen.blit(text, (x + self.cell_size / 2 - 10, y + self.cell_size + 20))

        for key in self.open_cells:
            i, j = key
            if self.BOARD[j][i] != '.':
                text = FONT_2.render(str(self.BOARD[j][i]), True, COLORS[9])
                screen.blit(text, (self.open_cells.get(key)[0] + self.cell_size / 2 - 10,
                                   self.open_cells.get(key)[1] + self.cell_size + 20))

        if self.win or self.lose:
            if self.win:
                word_1 = '         Поздравляем!!'
                word_2 = 'Далее'
                pygame.mixer.music.stop()
                sound1 = pygame.mixer.Sound('Victory Theme.ogg')
            else:
                word_1 = '        Вы проиграли...'
                word_2 = 'Еще раз'
                sound1 = pygame.mixer.Sound('Game Over Theme.ogg')

            rect = (140, 190, 300, 150)
            text = FONT_1.render(word_1, True, COLORS[9])

            sound1.set_volume(0.2)
            sound1.play()
            word_3 = FONT_3.render('Выход', True, COLORS[8])
            t3 = FONT_3.render(word_2, True, COLORS[8])

            AGAIN = pygame.Rect(160, 270, 100, 40)  # КНОПКА СТАРТА ИГРЫ
            EXIT = pygame.Rect(320, 270, 100, 40)  # КНОПКА ПРАВИЛА

            pygame.draw.rect(screen, COLORS[7], rect)
            pygame.draw.rect(screen, COLORS[8], rect, 5)

            pygame.draw.rect(screen, COLORS[0], AGAIN)
            pygame.draw.rect(screen, COLORS[0], EXIT)

            screen.blit(text, (150, 200))
            screen.blit(word_3, (330, 275))
            screen.blit(t3, (170, 275))
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if EXIT.collidepoint(event.pos):
                            sys.exit()
                        if AGAIN.collidepoint(event.pos):
                            if self.lose:  # судоку не меняется
                                for i in self.open_cells.keys():
                                    q2, q1 = i
                                    self.BOARD[q1][q2] = '.'
                                self.win = False
                                self.lose = False
                                run = False
                            elif self.win:
                                self.BOARD = read_sudoku(LEVELS[n + 1])
                                self.check_cells(screen)
                                self.win = False
                                self.lose = False
                                run = False

                    clock.tick(FPS)
                    pygame.display.flip()

    def get_cell(self, mouse_pos):  # получение координат нажатий мыши
        x1 = (mouse_pos[0] - self.left) // self.cell_size
        y1 = (mouse_pos[1] - self.top) // self.cell_size
        if x1 < 0 or x1 >= self.width or y1 < 0 or y1 >= self.height:
            return None
        return x1, y1

    def redraw_nums(self, x, y, text):  # при первом нажатии красим клетку в синий, при вводе числа - сохраняем в BOARD
        if text.isdigit() and len(text) < 2 and text != '0':
            self.BOARD[y][x] = int(text)
            return self.open_cells.get((x, y))

    def erase(self, x, y):
        self.BOARD[y][x] = '.'


# __________________________________________________ЗАСТАВКА_______________________________________________________#
def start_screen():
    START = pygame.Rect(200, 210, 200, 50)  # КНОПКА СТАРТА ИГРЫ
    RULES = pygame.Rect(200, 300, 200, 50)  # КНОПКА ПРАВИЛА
    FINISH = pygame.Rect(200, 390, 200, 50)  # КНОПКА ВЫХОД

    rules_img = pygame.image.load('rules.jpg')

    text1 = FONT_1.render('НАЧАТЬ', True, COLORS[0])
    text2 = FONT_1.render('ПРАВИЛА', True, COLORS[0])
    text3 = FONT_1.render('ВЫХОД', True, COLORS[0])

    img = pygame.image.load('fon.jpg')
    fon = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw():
        screen.blit(fon, (0, 0))

        pygame.draw.rect(screen, COLORS[3], START)
        pygame.draw.rect(screen, COLORS[3], RULES)
        pygame.draw.rect(screen, COLORS[3], FINISH)

        screen.blit(text1, (250, 225))
        screen.blit(text2, (240, 315))
        screen.blit(text3, (255, 405))

    draw()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_q:
                    draw()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if START.collidepoint(event.pos):
                    sound_click_1.play()
                    return
                if RULES.collidepoint(event.pos):
                    sound_click_1.play()
                    screen.blit(rules_img, (0, 0))
                if FINISH.collidepoint(event.pos):
                    sound_click_2.play()
                    sys.exit()

            clock.tick(FPS)

            pygame.display.flip()


# ________________________________________________________________________________________________________________#


# ____________________________________________________САМА ИГРА_____________________________________________________#


def main():
    board = Sudoku(9, 9)
    start_screen()
    board.check_cells(screen)
    running = True
    text = ""
    text_2 = FONT_1.render('Введите число:', True, COLORS[0])

    input_active = True
    text_pos = (400, 550)
    my_sprite = MySprite()

    my_group = pygame.sprite.Group(my_sprite)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = board.get_cell(event.pos)  # клетка, на которую нажали
                if pos:
                    x, y = pos
                    if event.button == 3:
                        sound_click_2.play()
                        board.erase(x, y)
                    if event.button == 1:
                        sound_click_1.play()
                        board.redraw_nums(x, y, text)  # координаты этой клетки

                    input_active = True
                    text = ""

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    sound_click_2.play()

                else:
                    sound_click_1.play()
                    text += event.unicode

        text_surf = FONT_1.render(text, True, COLORS[0])

        my_group.update()
        my_group.draw(screen)

        board.render(screen)

        screen.blit(text_surf, text_pos)
        screen.blit(text_2, (200, 550))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


main()
