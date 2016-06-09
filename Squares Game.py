
import pygame,sys,time,random
from pygame.locals import *
pygame.init()

boardx = 40
boardy = 20
size = 30
windx = size*boardx
windy = size*boardy
maxLabels = 10

cBlock = (0,0,0)
cBorder = (100,200,255)
cPlay = (255,255,255)
cGoal = (0,200,0)
cText = (255,255,255)
BG = (0,0,0)

def r():
    return random.randint(0,255)

colors = []
for i in range(0,maxLabels):
    colors.append((r(),r(),r()))

#Disco!

def cAir(label):
    return colors[label-1]

#Normal
"""
def cAir(label):
    colors = [(240, 2, 15), (95, 170, 18), (81, 70, 158), (132, 237, 234)]
    return colors[label-1]
"""
def write(phrase,color,size_word,center):
    font = pygame.font.Font('freesansbold.ttf',size_word)
    surf = font.render(phrase,True,color)
    rect = surf.get_rect()
    rect.center = center
    window.blit(surf,rect)

def blank():
    board = []
    for i in range(0,boardx):
        col = []
        for j in range(0,boardy):
            col.append(0)
        board.append(col)
    for i in range(0,boardy):
        board[0][i] = -1
        board[boardx-1][i] = -1
    for i in range(0,boardx):
        board[i][0] = -1
        board[i][boardy-1] = -1
    return board

def space(board):
    num = 0
    for i in board:
        for j in i:
            if j > 0:
                num+=1
    return num

def protoBoard(labels):
    sx = boardx/2
    sy = boardy/2
    sb = blank()
    sol = []
    while True:
        sb[sx][sy] +=1
        moves = []
        if -1 != sb[sx+1][sy] < labels:
            moves.append((1,0))
        if -1 != sb[sx-1][sy] < labels:
            moves.append((-1,0))
        if -1 != sb[sx][sy+1] < labels:
            moves.append((0,1))
        if -1 != sb[sx][sy-1] < labels:
            moves.append((0,-1))
        if moves == []:
            break
        direction = random.choice(moves)
        sol.append((sx,sy))
        dx,dy = direction
        sx+=dx
        sy+=dy
    return [sb,sx,sy,sol]

def randomBoard(labels,start,end):
    while True:
        proto = protoBoard(labels)
        if start<space(proto[0])<=end:
            return proto

def drawBoard(board):
    for i in range(0,boardx):
        for j in range(0,boardy):
            square = board[i][j]
            rect = (i*size,j*size,size,size)
            if square == 0:
                pygame.draw.rect(window,cBlock,rect,0)
            if square > 0:
                pygame.draw.rect(window,cAir(square),rect,0)
            if square == -1:
                pygame.draw.rect(window,cBorder,rect,0)

def char(xpos,ypos):
    pygame.draw.circle(window,cPlay,(xpos*size+size/2,ypos*size+size/2),size/3,0)

def drawGoal(xpos,ypos):
    pygame.draw.circle(window,cGoal,(xpos*size+size/2,ypos*size+size/2),size/3,0)

def disWin():
    write('You win!',cText,50,(windx/2,windy/2))

def win(board):
    num = 0
    for i in board:
        for j in i:
            if j > 0:
                num+=1
    if num == 1:
        return True
    return False

def solution(sol,xpos,ypos,cell,org):
    index = 0
    nums = 0
    xgo = xpos
    ygo = ypos
    for step in sol:
        if (xpos,ypos) == step and index<len(sol)-1:
            nums+=1
            if nums == org-cell+1:
                xgo,ygo = sol[index+1]
                pygame.draw.line(window,cPlay,(xpos*size+size/2,ypos*size+size/2),(xgo*size+size/2,ygo*size+size/2),3)
                break
        index+=1
    return (xgo-xpos,ygo-ypos)

def disSpaces(num):
    write(str(num),cBlock,20,(windx/2,windy-10))

def game(labels,start,end):
    ref = randomBoard(labels,start,end)
    board = []
    for i in ref[0]:
        row = []
        for j in i:
            row.append(j)
        board.append(row)
    xpos = boardx/2
    ypos = boardy/2
    spaces = space(board)
    won = False
    show = False
    running = True
    while running:
        u = d = l = r = False
        if board[xpos][ypos+1] > 0:
            d = True
        if board[xpos][ypos-1] > 0:
            u = True
        if board[xpos+1][ypos] > 0:
            r = True
        if board[xpos-1][ypos] > 0:
            l = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and l:
                    if show:
                        if sol == (-1,0):
                            board[xpos][ypos]-=1
                            xpos-=1
                    else:
                        board[xpos][ypos]-=1
                        xpos-=1
                elif event.key == K_RIGHT and r:
                    if show:
                        if sol == (1,0):
                            board[xpos][ypos]-=1
                            xpos+=1
                    else:
                        board[xpos][ypos]-=1
                        xpos+=1
                elif event.key == K_UP and u:
                    if show:
                        if sol == (0,-1):
                            board[xpos][ypos]-=1
                            ypos-=1
                    else:
                        board[xpos][ypos]-=1
                        ypos-=1
                elif event.key == K_DOWN and d:
                    if show:
                        if sol == (0,1):
                            board[xpos][ypos]-=1
                            ypos+=1
                    else:
                        board[xpos][ypos]-=1
                        ypos+=1
                elif event.key == K_r:
                    board = []
                    for i in ref[0]:
                        row = []
                        for j in i:
                            row.append(j)
                        board.append(row)
                    xpos = boardx/2
                    ypos = boardy/2
                    spaces = space(board)
                elif event.key == K_n and won:
                    running = False
                elif event.key == K_s:
                    if show:
                        show = False
                    else:
                        show = True
                elif event.key == K_q:
                    running = False
        drawBoard(board)
        drawGoal(ref[1],ref[2])
        char(xpos,ypos)
        disSpaces('Diffuculty: '+str(spaces*(2**labels)/2)+' Size: '+str(spaces))
        if show:
            sol = solution(ref[3],xpos,ypos,board[xpos][ypos],ref[0][xpos][ypos])
        if win(board) and (xpos,ypos) == (ref[1],ref[2]):
            disWin()
            won = True
        pygame.display.update()

def screen():
    window.fill(BG)
    write('Squares',cText,50,(windx/2,35))
    for i in range(1,maxLabels+1):
        write('Labels: '+str(i),cText,20,(windx/2,windy/4+i*25))
        pygame.draw.rect(window,cAir(i),(windx/2-100,windy/4-10+i*25,20,20),0)
    write('Press space to play.',cText,20,(windx/2,windy-25))

def choosed(label):
    pygame.draw.line(window,cAir(label),(0,label*25+windy/4-10),(windx,label*25+windy/4-10))
    pygame.draw.line(window,cAir(label),(0,label*25+windy/4+10),(windx,label*25+windy/4+10))

def restriction(start,end):
    write('Start: '+str(start),cText,20,(windx/4,windy/2))
    write('End: '+str(end),cText,20,(windx*3/4,windy/2))
    pygame.draw.polygon(window,cText,[(windx/4,windy/2-15),(windx/4+10,windy/2-15),(windx/4+5,windy/2-30)],0)
    pygame.draw.polygon(window,cText,[(windx/4,windy/2+15),(windx/4+10,windy/2+15),(windx/4+5,windy/2+30)],0)
    pygame.draw.polygon(window,cText,[(windx*3/4,windy/2-15),(windx*3/4+10,windy/2-15),(windx*3/4+5,windy/2-30)],0)
    pygame.draw.polygon(window,cText,[(windx*3/4,windy/2+15),(windx*3/4+10,windy/2+15),(windx*3/4+5,windy/2+30)],0)

def main():
    global window
    window = pygame.display.set_mode((windx,windy))
    pygame.display.set_caption('Squares')
    choose = 1
    start = 0
    end = 100
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex,mousey = event.pos
                for i in range(1,maxLabels+1):
                    if i*25+windy/4-10<mousey<i*25+windy/4+10 and windx/2-60<mousex<windx/2+60:
                        choose = i
                up = windy/2-30<mousey<windy/2-15
                down = windy/2+15<mousey<windy/2+30
                left = windx/4<mousex<windx/4+10
                right = windx*3/4<mousex<windx*3/4+10
                if up:
                    if left and end>start+20:
                        start+=10
                    if right:
                        end+=10
                if down:
                    if left:
                        start-=10
                    if right and end>start+20:
                        end-=10
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game(choose,start,end)
        screen()
        choosed(choose)
        restriction(start,end)
        pygame.display.update()

if __name__ == '__main__':
    main()
