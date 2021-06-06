import pygame
import random

s_width=800
s_height=600
p_width=300
p_height=200
block_size=30

topleft_x=(s_width-p_width) //2
topleft_y=s_height-p_height

#alakzatok
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#alakzat definicio

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255, 200,50),(255,200,250),(120,120,120)]

class darab(object):
        rows=20
        coloumns=10

        def __init__(self, coloumn, row, shape):
            self.x=coloumn
            self.y=row
            self.shape=shape
            self.color=shape.colors[shapes.index(shape)]
            self.rotation=0
def create_grid(locked_positions={}):
    grid=[[(0,0,0)] for x in range(10)] in range(20)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

#meghivas, atnevezesnel elromlik az egesz.
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

#helyvizsgalat
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

#uj forma letrehozasa
def get_shape():
    global shapes, shape_colors

    return darab(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('msoutlook', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    topleft_x + p_width / 2 - (label.get_width() / 2), topleft_y + p_height / 2 - label.get_height() / 2))
#Ezzel a szoveget iratjuk ki kozepen, kesobb van szerepe a jatek inditasanal es az esetleges kijatszas eseten.

def draw_grid(surface, row, col):
    sx = topleft_x
    sy = topleft_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + p_width, sy + i * 30))  # vizszintes
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + p_height))  # fuggoleges
def clear_rows(grid, locked):
    # vizsgaljuk, hogy az also sor folotti sor telivan-e hogy azoknak is megadhato legyen a torles.

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # acsusztatunk, poziciokat adunk be a foglalt helyeknek
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('msoutlook', 30)
    label = font.render('Kovetkezo elem', 1, (255,255,255))

    sx = topleft_x + p_width + 50
    sy = topleft_y + p_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))
def draw_window(surface):
    surface.fill((0,0,0))
    # cim meg ezek
    font = pygame.font('msoutlook', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label, (topleft_x + p_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topleft_x + j* 30, topleft_y + i * 30, 30, 30), 0)

    # itt kellene neki megoldania minden kiiratast, ez egy masolt reszlet, MIVEL NEKEM NEM AKAR MUKODNI
    #Hihetetlen mennyi szenvedes van ezzel a pygame-vel, hivatkozgatni kell ra es meg az ember ne legyen ideges

    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (topleft_x, topleft_y, p_width, p_height), 5)
    # pygame.display.update()
def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0
    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 4:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

    #itt esnek a cuccok. Talaltam egy hasonlo kodot a neten (persze bugos volt) tehat vagy 3 ora stack overflow utan egy kilencedikes jott be azzal az otlettel,
    #hogy heggesszem ossze oket. Szerintem Nagy Marcellnak jar az otos ezert a tippert.
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        current_piece.y += 1
        if not (valid_space(current_piece, grid)) and current_piece.y > 0:
            current_piece.y -= 1
            change_piece = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
            quit()

        if event.type == pygame.KEYDOWN: #alap erzekeles
            if event.key == pygame.K_LEFT: #balramozgas
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1

            elif event.key == pygame.K_RIGHT: #jobbra
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif event.key == pygame.K_UP: #forgas
                current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                if not valid_space(current_piece, grid):
                    current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
            if event.key == pygame.K_DOWN: #lefele mozgas alias speedup
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
    shape_pos = convert_shape_format(current_piece)

    #kirajzolas
    for i in range(len(shape_pos)):
        x, y = shape_pos[i]
        if y > -1:
            grid[y][x] = current_piece.color
    #Foldeteres:
    if change_piece:
        for pos in shape_pos:
            p = (pos[0], pos[1])
            locked_positions[p] = current_piece.color
        current_piece = next_piece
        next_piece = get_shape()
        change_piece = False

        if clear_rows(grid, locked_positions): #Ha foldeter kigyulik a sor, akkor pontot kap
            score += 10

    draw_window(win)
    draw_next_shape(next_piece, win)
    pygame.display.update()

    if check_lost(locked_positions):#hamar nem lenne kitorolheto sor
        run = False

    draw_text_middle("Vesztettel", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    run = True #jatek inditasa
    while run:
        win.fill((0,0,0))
        draw_text_middle('nyomj egy gombot az inditashoz.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris .')

main_menu()