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
    animate = False
    loadimages()
    running = True
    sqselected = ()
    playerclicks = []
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
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
                                animate = True
                                sqselected = ()
                                playerclicks = []
                        if not moveMade:
                            playerclicks = [sqselected]
            elif e.type == p.KEYDOWN:
                if(e.key == p.K_z):
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if(e.key == p.K_r):
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqselected =[]
                    playerclicks = []
                    moveMade = False
                    animate =  False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqselected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by Checkmate')
            else:
                drawText(screen, 'White wins by Checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b') :
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('grey'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('grey'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



def drawGameState(screen, gs, validMoves, sqSelected): 
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    color1=(250, 250, 250)
    color2=(41, 109, 58 )
    colors = [color1, color2]
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


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount):
        r, c = ((move.startRow + dR*frame/frameCount), (move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen , color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, True, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__": 
    main()
