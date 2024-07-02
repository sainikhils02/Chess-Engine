import chessEngine
import pygame as p

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15
IMAGES={}


def loadimages():
    pieces = ['bR','bN','bB','bQ','bK','bB','bN','bR','bp','wp','wR','wN','wB','wQ','wK','wB','wN','wR']
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs=chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadimages()
    running = True
    sqselected = ()
    playerclicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1]//SQ_SIZE
                col = location[0]//SQ_SIZE
                if((row, col) == sqselected):
                    sqselected = ()
                    playerclicks = []
                else: 
                    sqselected = (row, col)
                    playerclicks.append(sqselected)
                if(len(playerclicks)==2):
                    move = chessEngine.Move(playerclicks[0], playerclicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            print(validMoves[i].getChessNotation())
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqselected = ()
                            playerclicks = []
                    if not moveMade:
                        playerclicks = [sqselected]
            elif e.type == p.KEYDOWN:
                if(e.key == p.K_z):
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs): 
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    color1=(250, 250, 250)
    color2=(41, 109, 58 )
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = color2 if (row+col)%2 else color1
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__": 
    main()
