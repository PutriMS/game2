import pygame
from pygame.locals import *
import random
pygame.init()

width = 400
height = 400
scoreboard_height = 25
window_size = (width,height + scoreboard_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three')

candy_colors = ['biru','ijo','oren','mera','ungu','kuning','orenn']
candy_width = 40
candy_height = 40
candy_size = (candy_width,candy_height)
class Candy:
    def __init__(self,row_num,col_num):
        self.row_num = row_num
        self.col_num = col_num

        self.color = random.choice(candy_colors)
        image_name = f'{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image,candy_size)#bwt gmbr lbh bgus
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num* candy_height

    def draw(self):
        screen.blit(self.image,self.rect)
    def snap(self):
        self.snap_row()
        self.snap_col()
    def snap_row(self):
        self.rect.top = self.row_num * candy_height
    def snap_col(self):
        self.rect.left = self.col_num*candy_width

board = []
for row_num in range(height//candy_height):
    board.append([])#buat bris kosong
    for col_num in range (width//candy_width):
        candy = Candy(row_num,col_num)#buat permen
        board[row_num].append(candy)#munculin permen ke bris
def draw():
    pygame.draw.rect(screen,(173,216,230),(0,0,width,height+scoreboard_height))

    for row in board:
        for candy in row:
            candy.draw()
    font = pygame.font.SysFont('monoface',18)
    score_text = font.render(f'Score = {score}',1,(0,0,0))
    score_text_rect = score_text.get_rect(center=(width/4,height+scoreboard_height/2))
    screen.blit(score_text,score_text_rect)

    moves_text = font.render(f'Moves = {moves}',1,(0,0,0))
    moves_text_rect = moves_text.get_rect(center=(width*3/4,height+scoreboard_height/2))
    screen.blit(moves_text,moves_text_rect)

def swap(candy1,candy2):
    temp_row = candy1.row_num
    temp_col = candy1.col_num
    candy1.row_num = candy2.row_num
    candy1.col_num = candy2.col_num
    candy2.row_num = temp_row
    candy2.col_num = temp_col
    #update
    board[candy1.row_num][candy1.col_num] = candy1
    board[candy2.row_num][candy2.col_num] = candy2
    candy1.snap()
    candy2.snap()

def find_matches(candy,matches):
    matches.add(candy)
    if candy.row_num > 0:#dkpling atas
        neighbor = board[candy.row_num-1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor,matches))
    if candy.row_num < height/candy_height-1:#bknpling bwh
        neighbor = board[candy.row_num+1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor,matches))
    if candy.col_num >0: #bkn pling kri
        neighbor = board[candy.row_num][candy.col_num -1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor,matches))

    if candy.col_num < width/candy_width-1: #bkn plg knn
        neighbor = board[candy.row_num][candy.col_num+1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor,matches))
    return matches

def match_three(candy):
    matches = find_matches(candy,set())
    if len(matches >= 3):
        return matches
    else:
        return set()
    
clicked_candy = None
swapped_candy = None
click_x = None
click_y = None

score = 0
moves = 0
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
            for row in board:
                for candy in row:
                    if candy.rect.collidepoint(event.pos):
                        clicked_candy = candy
                        click_x = event.pos[0]
                        click_y = event.pos[1]
        if clicked_candy is not None and event.type == MOUSEMOTION:
            distance_x = abs(click_x - event.pos[0])
            distance_y =abs(click_y - event.pos[1]#abs bwt spy dk - , event pos 0 = x pas player grk , 1 = y
            )
            if swapped_candy is not None:
                swapped_candy.snap()
            if distance_x>distance_y and click_x > event.pos[0]:
                direction = 'left'
            elif distance_x>distance_y and click_x < event.pos[0]:
                direction = 'right'
            elif distance_y>distance_x and click_y > event.pos[1]:
                direction ='up'
            else:
                direction='down'
                
            if direction in ['left','right']:
                clicked_candy.snap_row()
            else:
                clicked_candy.snap_col()
    draw()
    pygame.display.update()
pygame.quit()