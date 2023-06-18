import sys
import time
import pygame

class Button:
    def __init__(self,width:int,height:int,coordinates:tuple[int,int],textSize:int):
        self.__width=width
        self.__height=height
        self.__x=coordinates[0]
        self.__y=coordinates[1]
        self.__textSize=textSize
        self.__text=""
    def draw(self,screen:pygame.Surface):
        pygame.draw.rect(screen,(0,0,0),(self.__x,self.__y,self.__width,self.__height),4)
        pygame.draw.rect(screen,(255,255,255),(self.__x+4,self.__y+4,self.__width-8,self.__height-8))
        if self.__text!="":
            font=pygame.font.SysFont('italicc',self.__textSize)
            text=font.render(self.__text,True,(0,0,0))
            screen.blit(text,(self.__x + (self.__width/2 - text.get_width()/2), self.__y + (self.__height/2 - text.get_height()/2)))
    def isMouseOn(self,pos:tuple[int,int])->bool:
        return (pos[0]>self.__x and pos[0]<self.__x+self.__width) and (pos[1]>self.__y and pos[1]<self.__y+self.__height)
    def changeText(self,text:str):     
        self.__text=text
    def isEmpty(self)->bool:
        return self.__text==""
    def getText(self)->str:
        return self.__text

class Label:
    def __init__(self,text:str,font:str,size:int,coordinatesText:tuple[int,int]):
        self.__font=font,
        self.__size=size
        self.__text=text
        self.__x=coordinatesText[0]
        self.__y=coordinatesText[1]

    def drawLabel(self,screen:pygame.Surface):
        font=pygame.font.SysFont(self.__font,self.__size)      
        text=font.render(self.__text,True,(255,255,255))
        screen.blit(text,(self.__x + len(self.__text), self.__y + self.__size))

    def changeText(self,newText:str):
        self.__text=newText


def evaluate(b:list[list[Button]])->int :
    player, opponent = 'o', 'x'
    for row in range(3) :    
        if (b[row][0].getText() == b[row][1].getText() and b[row][1].getText() == b[row][2].getText() and not b[row][0].isEmpty()) :       
            if b[row][0].getText() == player :
                return 10
            elif b[row][0].getText() == opponent :
                return -10

    for col in range(3) :
        if (b[0][col].getText() == b[1][col].getText() and b[1][col].getText() == b[2][col].getText() and not b[0][col].isEmpty()) :         
            if b[0][col].getText() == player :
                return 10
            elif b[0][col].getText() == opponent :
                return -10

    if b[0][0].getText() == b[1][1].getText() and b[1][1].getText() == b[2][2].getText() and not b[0][0].isEmpty() :
        if b[0][0].getText() == player :
            return 10
        elif b[0][0].getText() == opponent :
            return -10
 
    if b[0][2].getText() == b[1][1].getText() and b[1][1].getText() == b[2][0].getText() and not b[0][2].isEmpty() :
        if b[0][2].getText() == player :
            return 10
        elif b[0][2].getText() == opponent :
            return -10
    return 0

def minimax(board:list[list[Button]], isMax:bool)->int :
    player, opponent = 'o', 'x'
    score = evaluate(board)
    if score == 10 :
        return score
    if score == -10 :
        return score
    if not IsThereFreeSquare(board):
        return 0
    if isMax:    
        best = -1000
        for i in range(3) :        
            for j in range(3) :
                if board[i][j].isEmpty():
                    board[i][j].changeText(player)
                    best = max(best, minimax(board,not isMax))
                    board[i][j].changeText('')
        return best
    else :
        best = 1000
        for i in range(3) :        
            for j in range(3) :
                if board[i][j].isEmpty():
                    board[i][j].changeText(opponent)
                    best = min(best, minimax(board, not isMax))
                    board[i][j].changeText('')
        return best

def computerMove(board:list[list[Button]])->list[list[Button]]:
    player='o'
    bestVal = -1000
    bestMove = (-1, -1)
    for i in range(3) :    
        for j in range(3) :
            if board[i][j].isEmpty():
                board[i][j].changeText(player)
                moveVal = minimax(board, False)
                board[i][j].changeText('')
                if moveVal > bestVal:               
                    bestMove = (i, j)
                    bestVal = moveVal
    board[bestMove[0]][bestMove[1]].changeText('o')
    return board

def IsThereFreeSquare(board:list[list[Button]])->bool:
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col].isEmpty():
                return True
    return False

def drawScreen(grid:list[list[Button]],labels:list[Label],screen:pygame.Surface):
    screen.fill((96, 130, 182))
    for r in grid:
        for b in r:
            b.draw(screen)
    for l in labels:
        l.drawLabel(screen)
    pygame.display.update()

def findButton(grid:list[list[Button]],mousepos):
    for row in range(0,3):
        for col in range(0,3):
            if grid[row][col].isMouseOn(mousepos):
                return (row,col)
    if grid[3][0].isMouseOn(mousepos):
        return (3,0)
    return (-1,-1)

def newGrid()->list[list[Button]]:
    grid=[
        [Button(200,200,(100,100),200),Button(200,200,(300,100),200),Button(200,200,(500,100),200)],
        [Button(200,200,(100,300),200),Button(200,200,(300,300),200),Button(200,200,(500,300),200)],
        [Button(200,200,(100,500),200),Button(200,200,(300,500),200),Button(200,200,(500,500),200)],
        [Button(500,250,(750,450),88)]
        ]     
    grid[3][0].changeText("Restart")
    return grid

def newLabels()->list[Label]:
    return [Label("Computer Wins: 0",'italicc',36,(750,200))
            ,Label("Player Wins: 0",'italicc',36,(750,270))
            ,Label("Draw: 0",'italicc',36,(750,340))]

def InitalizeScreen()->pygame.Surface:
    pygame.init()
    screen=pygame.display.set_mode((1350,900))
    pygame.display.set_caption("Tic Tac Toe")
    icon=pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    screen.fill((96, 130, 182))
    return screen

def checkIsGameWon(grid:list[list[Button]],winSymbol:str):
    for c in range(3):
        if grid[0][c].getText()==grid[1][c].getText() and grid[1][c].getText()==grid[2][c].getText() and grid[0][c].getText()==winSymbol:
           return True
    for r in range(3):
        if grid[r][0].getText()==grid[r][1].getText() and grid[r][1].getText()==grid[r][2].getText() and grid[r][0].getText()==winSymbol:
            return True
    if grid[0][0].getText()==grid[1][1].getText() and grid[1][1].getText()==grid[2][2].getText() and grid[0][0].getText()==winSymbol:
        return True
    if grid[0][2].getText()==grid[1][1].getText() and grid[1][1].getText()==grid[2][0].getText() and grid[0][2].getText()==winSymbol:
        return True                                                                        
    return False

if __name__ == "__main__":
    grid:list[list[Button]]=newGrid()
    labels:list[Label]=newLabels()
    screen:pygame.Surface=InitalizeScreen()
    turn=True
    mustItBeRestarted=False
    playerWins,computerWins,draws=0,0,0
    while True:        
        drawScreen(grid,labels,screen)      
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                sys.exit()      
            if e.type==pygame.MOUSEBUTTONDOWN:
                mousepos=pygame.mouse.get_pos()
                buttoncoords=findButton(grid,mousepos)
                if buttoncoords==(-1,-1):
                    continue           
                if turn:
                    if buttoncoords==(3,0):
                        turn=True
                        grid=newGrid()
                        mustItBeRestarted=False
                        continue
                    if not mustItBeRestarted and grid[buttoncoords[0]][buttoncoords[1]].isEmpty():
                        grid[buttoncoords[0]][buttoncoords[1]].changeText('x')
                        turn=False
        if mustItBeRestarted:
            continue
        if checkIsGameWon(grid,'x'):
            mustItBeRestarted=True
            playerWins+=1
            labels[1].changeText(f"Player Wins: {playerWins}")
            turn=True
            continue
        if not IsThereFreeSquare(grid):
            mustItBeRestarted=True
            draws+=1
            labels[2].changeText(f"Draw: {draws}")
            turn=True
            continue       
        drawScreen(grid,labels,screen)               
        if not turn:                                           
            grid=computerMove(grid)
            turn=True
            time.sleep(0.5)
        if checkIsGameWon(grid,'o'):
            mustItBeRestarted=True
            computerWins+=1
            labels[0].changeText(f"Computer Wins: {computerWins}")
            turn=True
            continue                            
