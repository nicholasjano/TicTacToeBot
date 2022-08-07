##########################################################
# This is a Tic Tac Toe bot, where you can verse it either
# starting or going second. The bot is trained by an
# algorith I created. With perfect play from the user,
# every game will end up in a draw. The bot will convert
# any winning position. If you need help, there is a help
# button that shows your next best move. The game is
# downloaded pre-trained, but if you'd like to retrain it
# yourself, empty the simulations.txt file and train.
#
# Made by Nick Jano.
##########################################################

import pygame
from pygame import mixer
from random import randint
import os
import math
import webbrowser

pygame.init()
mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (77, 160, 211)
DARK_GREEN = (8, 166, 25)

defaultFont = pygame.font.SysFont('Courier', 30, bold=True)

winSound = mixer.Sound('tada.wav')
mixer.Sound.set_volume(winSound, 0.8)
lossSound = mixer.Sound('loss.wav')
mixer.Sound.set_volume(lossSound, 0.4)

gamesSimulated = 0
testedBefore = False
savedMoves = [[], []]
players = [['X', []], ['O', []]]
board = ['1', '2', '3',
         '4', '5', '6',
         '7', '8', '9']
boardThisTurn = []
boardThisTurnHelp = []
winPos = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9'],
          ['1', '5', '9'], ['3', '5', '7']]
userWins, AIWins, draws = 0, 0, 0


def drawButton(win, text, r, bColour, fColour, font):
    pygame.draw.rect(win, bColour, r)
    pygame.draw.rect(win, fColour, r, 3)
    textSurface = font.render(text, True, fColour)
    win.blit(textSurface, (r[0] + (r[2] - textSurface.get_width()) // 2, r[1] + (r[3] - textSurface.get_height()) // 2))


def drawButtons(win, buttons, textList, Colour, font):
    for i, r in enumerate(buttons):
        drawButton(win, textList[i], r, Colour, BLACK, font)


def getButtonIndex(bList, mp):
    for i, r in enumerate(bList):
        if pygame.Rect(r).collidepoint(mp):
            return i
    return -1


def blitText(message, font, fontSize, x, y, bold, center=True):
    defaultFont = pygame.font.SysFont(font, fontSize, bold=bold)
    textSurface = defaultFont.render(message, True, BLACK)
    if center:
        x = win.get_width() // 2 - textSurface.get_width() // 2
    win.blit(textSurface, (x, y))


def readFiles(fileName):
    file = []
    fi = open(fileName + '.txt', 'r')
    for line in fi:
        file.append(line.strip())
    return file


def redraw_game_window(currentScreen):
    global start_ticks, minutes
    if currentScreen == START_SCREEN:
        win.fill(DARK_GREEN)
        blitText('Tic-Tac-Toe AI', 'Courier', 75, 0, 100, True, center=True)
        blitText('By Nick Jano', 'Courier', 50, 0, 200, True, center=True)
        drawButtons(win, buttonsStart, buttonsStartText, LIGHT_BLUE, defaultFont)
        if not trainedBefore and (pygame.time.get_ticks()-start_ticks)/1000 < 3:
            blitText('You need to train the AI before you can play', 'Courier', 30, 0, 280, True, center=True)
    elif currentScreen == SIM_SCREEN:
        win.fill(LIGHT_BLUE)
        timeElapsed = math.floor((pygame.time.get_ticks()-start_ticks)/1000)
        if timeElapsed >= 60:
            minutes += 1
            start_ticks = pygame.time.get_ticks()
        elif timeElapsed < 10:
            timeElapsed = (f'0{timeElapsed}')
        blitText('Time Elapsed: {}:{}m'.format(minutes, timeElapsed), 'Courier', 30, 10, 10, True, center=False)
        blitText('AI TRAINING', 'Courier', 75, 0, 100, True, center=True)
        blitText('AI SIMULATION WORKING', 'Courier', 50, 0, win.get_height() // 2 - 225, True, center=True)
        blitText('GAMES SIMULATED: {}'.format(gamesSimulated), 'Courier', 50, 0, win.get_height() // 2 - 155, True, center=True)
        blitText('Once Games Simulated is > 50000,', 'Courier', 40, 0, win.get_height() // 2 - 70, True, center=True)
        blitText('the AI should be 99% trained.', 'Courier', 40, 0, win.get_height() // 2 - 15, True, center=True)
        blitText('More training = better AI.', 'Courier', 40, 0, win.get_height() // 2 + 40, True, center=True)
        if gamesSimulated < 50000:
            drawButton(win, 'Cancel Training', buttonSIM, RED, BLACK, defaultFont)
        else:
            drawButton(win, 'Done', buttonSIM, GREEN, BLACK, defaultFont)
        blitText('You will only need to do this once', 'Courier', 40, 0, 662, True, center=True)
        blitText('becuase the data will be saved.', 'Courier', 40, 0, 717, True, center=True)
        blitText('ETA from 0-50000: ~15-20 mins', 'Courier', 40, 0, 797, True, center=True)
    elif currentScreen == AIOFFENCE_SCREEN:
        win.fill(DARK_GREEN)
        pygame.draw.line(win, BLACK, (win.get_width() // 2 - 106, 73), (win.get_width() // 2 - 106, 692), 10)
        pygame.draw.line(win, BLACK, (win.get_width() // 2 + 104, 73), (win.get_width() // 2 + 104, 692), 10)
        pygame.draw.line(win, BLACK, (140, win.get_width() // 2 - 173), (759, win.get_width() // 2 - 173), 10)
        pygame.draw.line(win, BLACK, (140, win.get_width() // 2 + 37), (759, win.get_width() // 2 + 37), 10)
        drawButton(win, 'Help', (win.get_width() // 2 - 100, 765, 200, 100), LIGHT_BLUE, BLACK, defaultFont)
        blitText('Stats:', 'Courier', 30, 60, 740, True, center=False)
        blitText('User Wins: {}'.format(userWins), 'Courier', 30, 60, 770, True, center=False)
        blitText('AI Wins:   {}'.format(AIWins), 'Courier', 30, 60, 800, True, center=False)
        blitText('Draws:     {}'.format(draws), 'Courier', 30, 60, 830, True, center=False)
        for hMove in helpMoves:
            if boardThisTurnHelp == board:
                win.blit(images[3], hMove)
            else:
                helpMoves.clear()
        for i, num in enumerate(board):
            if num == 'X':
                win.blit(images[0], (buttonsGame[i][0], buttonsGame[i][1]))
            elif num == 'O':
                win.blit(images[1], (buttonsGame[i][0], buttonsGame[i][1]))
        if yourMove:
            blitText('Your Turn', 'Courier', 30, 0, 10, True, center=True)
        if boardThisTurn == board and yourMove and (pygame.time.get_ticks()-start_ticks)/1000 < 3:
            blitText('You cannot move there.', 'Courier', 30, 0, 720, True, center=True)
        if checkWinner() is not None:
            blitText('Play Again?', 'Courier', 30, 620, 740, True, center=False)
            drawButtons(win, buttonsPA, buttonsPAText, LIGHT_BLUE, defaultFont)
    elif currentScreen == AIDEFENCE_SCREEN:
        win.fill(DARK_GREEN)
        pygame.draw.line(win, BLACK, (win.get_width() // 2 - 106, 73), (win.get_width() // 2 - 106, 692), 10)
        pygame.draw.line(win, BLACK, (win.get_width() // 2 + 104, 73), (win.get_width() // 2 + 104, 692), 10)
        pygame.draw.line(win, BLACK, (140, win.get_width() // 2 - 173), (759, win.get_width() // 2 - 173), 10)
        pygame.draw.line(win, BLACK, (140, win.get_width() // 2 + 37), (759, win.get_width() // 2 + 37), 10)
        drawButton(win, 'Help', (win.get_width() // 2 - 100, 765, 200, 100), LIGHT_BLUE, BLACK, defaultFont)
        blitText('Stats:', 'Courier', 30, 60, 740, True, center=False)
        blitText('User Wins: {}'.format(userWins), 'Courier', 30, 60, 770, True, center=False)
        blitText('AI Wins:   {}'.format(AIWins), 'Courier', 30, 60, 800, True, center=False)
        blitText('Draws:     {}'.format(draws), 'Courier', 30, 60, 830, True, center=False)
        for hMove in helpMoves:
            if boardThisTurnHelp == board:
                win.blit(images[2], hMove)
            else:
                helpMoves.clear()
        for i, num in enumerate(board):
            if num == 'X':
                win.blit(images[0], (buttonsGame[i][0], buttonsGame[i][1]))
            elif num == 'O':
                win.blit(images[1], (buttonsGame[i][0], buttonsGame[i][1]))
        if yourMove:
            blitText('Your Turn', 'Courier', 30, 0, 10, True, center=True)
        if boardThisTurn == board and yourMove and (pygame.time.get_ticks()-start_ticks)/1000 < 3:
            blitText('You cannot move there.', 'Courier', 30, 0, 720, True, center=True)
        if checkWinner() is not None:
            blitText('Play Again?', 'Courier', 30, 620, 740, True, center=False)
            drawButtons(win, buttonsPA, buttonsPAText, LIGHT_BLUE, defaultFont)
    elif currentScreen == HELP_SCREEN:
        win.fill(DARK_GREEN)
        blitText('HELP', 'Courier', 75, 0, 50, True, center=True)
        pygame.draw.line(win, BLACK, (360, 125), (536, 125), 7)
        drawButtons(win, buttonsHelp, buttonsHelpText, LIGHT_BLUE, defaultFont)
        blitText('Train AI', 'Courier', 50, 0, 150, True, center=True)
        textDistance = 210
        for text in trainAIHelp:
            blitText(text, 'Courier', 30, 0, textDistance, False, center=True)
            textDistance += 30
        textDistance += 30
        blitText('Verse Offence AI', 'Courier', 50, 0, textDistance, True, center=True)
        textDistance += 60
        for text in VSAIOffenceHelp:
            blitText(text, 'Courier', 30, 0, textDistance, False, center=True)
            textDistance += 30
        textDistance += 30
        blitText('Verse Defence AI', 'Courier', 50, 0, textDistance, True, center=True)
        textDistance += 60
        for text in VSAIDefenceHelp:
            blitText(text, 'Courier', 30, 0, textDistance, False, center=True)
            textDistance += 30
    pygame.display.update()


def finalListEdits(winner, savedMoves, boardsPlayed):
    if winner == 'X':
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[0]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for xMove in players[0][1]:
                        if xMove in boardPlayed:
                            if xMove == players[0][1][-1]:
                                moveCounter = 0
                                for i, bMove in enumerate(move[1]):
                                    moveCounter += 1
                                    if moveCounter % 2 == 1:
                                        move[1][i] = 500
                                move[1][move[1].index(xMove) + 1] = 2000
                            else:
                                move[1][move[1].index(xMove) + 1] += 3
                                if move[1][move[1].index(xMove) + 1] > 2000:
                                    move[1][move[1].index(xMove) + 1] = 2001
                                    moveCounter = 0
                                    for i, bMove in enumerate(move[1]):
                                        moveCounter += 1
                                        if moveCounter % 2 == 1:
                                            move[1][i] -= 1   # maybe -2?
                                            if move[1][i] < 500:  # make these 1
                                                move[1][i] = 500  # for the old results (or 5)
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[1]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for oMove in players[1][1]:
                        if oMove in boardPlayed:
                            move[1][move[1].index(oMove) + 1] -= 1
                            if move[1][move[1].index(oMove) + 1] < 500:
                                move[1][move[1].index(oMove) + 1] = 500
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break
    elif winner == 'O':
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[1]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for oMove in players[1][1]:
                        if oMove in boardPlayed:
                            if oMove == players[1][1][-1]:
                                moveCounter = 0
                                for i, bMove in enumerate(move[1]):
                                    moveCounter += 1
                                    if moveCounter % 2 == 1:
                                        move[1][i] = 500
                                move[1][move[1].index(oMove) + 1] = 2000
                            else:
                                move[1][move[1].index(oMove) + 1] += 3
                                if move[1][move[1].index(oMove) + 1] > 2000:
                                    move[1][move[1].index(oMove) + 1] = 2001
                                    moveCounter = 0
                                    for i, bMove in enumerate(move[1]):
                                        moveCounter += 1
                                        if moveCounter % 2 == 1:
                                            move[1][i] -= 1
                                            if move[1][i] < 500:
                                                move[1][i] = 500
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[0]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for xMove in players[0][1]:
                        if xMove in boardPlayed:
                            move[1][move[1].index(xMove) + 1] -= 1
                            if move[1][move[1].index(xMove) + 1] < 500:
                                move[1][move[1].index(xMove) + 1] = 500
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break
    else:
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[1]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for oMove in players[1][1]:
                        if oMove in boardPlayed:
                            move[1][move[1].index(oMove) + 1] += 1
                            if move[1][move[1].index(oMove) + 1] > 2000:
                                move[1][move[1].index(oMove) + 1] = 2001
                                moveCounter = 0
                                for i, bMove in enumerate(move[1]):
                                    moveCounter += 1
                                    if moveCounter % 2 == 1:
                                        move[1][i] -= 1
                                        if move[1][i] < 500:
                                            move[1][i] = 500
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break
        for boardPlayed in boardsPlayed:
            nextBoard = False
            for move in savedMoves[0]:
                if nextBoard: break
                elif move[0] == boardPlayed:
                    for xMove in players[0][1]:
                        if xMove in boardPlayed:
                            move[1][move[1].index(xMove) + 1] += 1
                            if move[1][move[1].index(xMove) + 1] > 2000:
                                move[1][move[1].index(xMove) + 1] = 2001
                                moveCounter = 0
                                for i, bMove in enumerate(move[1]):
                                    moveCounter += 1
                                    if moveCounter % 2 == 1:
                                        move[1][i] -= 1
                                        if move[1][i] < 500:
                                            move[1][i] = 500
                            move[1][0] = sum(move[1][2::2])
                            nextBoard = True
                            break


def checkWinner():  # returns None if no winner
    for player in players:
        for win in winPos:
            if win[0] in player[1] and win[1] in player[1] and win[2] in player[1]:
                return player[0]
    if len(players[0][1]) + len(players[1][1]) == 9:
        return 'draw'


def AISimulation():
    boardPos = 0
    move = 10
    boardsPlayed = []
    gameOn = True
    while gameOn:
        for i in range(2):
            boardSaved = False
            if checkWinner() is not None:
                finalListEdits(checkWinner(), savedMoves, boardsPlayed)
                gameOn = False
                break
            else:
                for savedBoard in savedMoves[i]:
                    if ''.join(board) == savedBoard[0]:
                        boardPos = savedMoves[i].index(savedBoard)
                        boardSaved = True
                        break
                if boardSaved:
                    moveRand = randint(1, savedMoves[i][boardPos][1][0])
                    for j, num in enumerate(savedMoves[i][boardPos][1][2::2]):
                        moveRand -= num
                        if moveRand <= 0:
                            move = savedMoves[i][boardPos][1][1::2][j]
                            break
                else:
                    possibleMovesCounter = 0
                    possibleMoves = []
                    for boardNum in board:
                        if boardNum.isdigit():
                            possibleMoves.extend((boardNum, 500))
                            possibleMovesCounter += 500
                    possibleMoves.insert(0, possibleMovesCounter)
                    savedMoves[i].append([''.join(board), possibleMoves])
                    moveRand = randint(1, (possibleMovesCounter/500))
                    for j, num in enumerate(savedMoves[i][-1][1][2::2]):
                        moveRand -= (num/500)
                        if moveRand <= 0:
                            move = savedMoves[i][-1][1][1::2][j]
                            break
                boardsPlayed.append(''.join(board))
                board[int(move) - 1] = players[i][0]
                players[i][1].append(move)


monitorInfo = pygame.display.Info()
x = monitorInfo.current_w / 2 - 450
y = monitorInfo.current_h / 2 - 450
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
win = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Tic-Tac-Toe AI by Nick Jano')
images = [pygame.image.load('X.png'), pygame.image.load('O.png'), pygame.image.load('XRed.png'), pygame.image.load('ORed.png')]
pygame.display.set_icon(pygame.image.load('XIcon.jpg'))
buttonsStart = ((win.get_width() // 2 - 150, 350, 300, 100), (win.get_width() // 2 - 400, 525, 300, 100),
                (win.get_width() // 2 + 100, 525, 300, 100), (win.get_width() // 2 - 150, 700, 300, 100))
buttonsStartText = ['Train AI', 'Verse Offence AI', 'Verse Defence AI', 'Help']
buttonSIM = (win.get_width() // 2 - 150, 550, 300, 100)
buttonsHelp = ((50, 50, 200, 100), (win.get_width() // 2 - 225, 740, 450, 100))
buttonsHelpText = ['Back', 'How to play Tic-Tac-Toe']
trainAIHelp = ['The AI needs to be trained to play',
               'Tic-Tac-Toe before you can verse it.',
               'To Train, just press the "Train AI"',
               'button on the home screen.',
               'It will play hundreds of games a second until',
               'it has fully learned the game.']
VSAIOffenceHelp = ['Play VS the AI, (AI Starts)',
                   'AI is X, you are O']
VSAIDefenceHelp = ['Play VS the AI, (You Start)',
                   'You are X, AI is O']
buttonsGame = ((win.get_width() // 2 - 310, 73, 200, 200),
               (win.get_width() // 2 - 100, 73, 200, 200), (win.get_width() // 2 + 110, 73, 200, 200),
               (win.get_width() // 2 - 310, 283, 200, 200),
               (win.get_width() // 2 - 100, 283, 200, 200), (win.get_width() // 2 + 110, 283, 200, 200),
               (win.get_width() // 2 - 310, 493, 200, 200),
               (win.get_width() // 2 - 100, 493, 200, 200), (win.get_width() // 2 + 110, 493, 200, 200),
               (win.get_width() // 2 - 150, 700, 300, 150))
buttonsPA = ((630, 795, 75, 50), (725, 795, 75, 50))
buttonsPAText = ['Yes', 'No']
helpMoves = []
trainedBefore = True
yourMove = False
added = False
START_SCREEN = 1
SIM_SCREEN = 2
AIOFFENCE_SCREEN = 3
AIDEFENCE_SCREEN = 4
HELP_SCREEN = 5
currentScreen = START_SCREEN
inPlay = True
while inPlay:
    redraw_game_window(currentScreen)
    #pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            if currentScreen == START_SCREEN:
                bIndex = getButtonIndex(buttonsStart, clickPos)
                if bIndex != -1:
                    if bIndex == 0:
                        currentScreen = SIM_SCREEN
                        minutes = 0
                        try:
                            savedMoves = eval(readFiles('simulations')[0])
                            gamesSimulated = eval(readFiles('simulations')[1])
                        except:
                            pass
                        start_ticks = pygame.time.get_ticks()
                    elif bIndex == 1:
                        try:
                            savedMoves = eval(readFiles('simulations')[0])
                            currentScreen = AIOFFENCE_SCREEN
                            yourMove = False
                        except:
                            start_ticks = pygame.time.get_ticks()
                            trainedBefore = False
                    elif bIndex == 2:
                        try:
                            savedMoves = eval(readFiles('simulations')[0])
                            currentScreen = AIDEFENCE_SCREEN
                            yourMove = True
                        except:
                            start_ticks = pygame.time.get_ticks()
                            trainedBefore = False
                    elif bIndex == 3:
                        currentScreen = HELP_SCREEN
            elif currentScreen == SIM_SCREEN:
                if pygame.Rect(buttonSIM).collidepoint(clickPos):
                    if gamesSimulated < 50000:
                        gamesSimulated = 0
                        currentScreen = START_SCREEN
                    else:
                        f = open('simulations.txt', 'w+')
                        savedMoves[0][0][1][10] = 1800
                        savedMoves[0][0][1][0] = sum(savedMoves[0][0][1][2::2])
                        f.write(f'{savedMoves}\n{gamesSimulated}')
                        currentScreen = START_SCREEN
            elif currentScreen == AIOFFENCE_SCREEN:
                if checkWinner() is None:
                    bIndex = getButtonIndex(buttonsGame, clickPos)
                    if bIndex != -1:
                        if yourMove:
                            if bIndex != 9:
                                if str(bIndex + 1) in board:
                                    board[bIndex] = players[1][0]
                                    players[1][1].append(str(bIndex + 1))
                                    yourMove = False
                                else:
                                    boardThisTurn = board[:]
                                    start_ticks = pygame.time.get_ticks()
                            else:
                                boardPos = 0
                                boardSaved = False
                                move = 10
                                for savedBoard in savedMoves[1]:
                                    if ''.join(board) == savedBoard[0]:
                                        boardPos = savedMoves[1].index(savedBoard)
                                        boardSaved = True
                                        break
                                if boardSaved:
                                    max = 0
                                    for j, num in enumerate(savedMoves[1][boardPos][1][2::2]):
                                        if num > max:
                                            max = num
                                            move = savedMoves[1][boardPos][1][1::2][j]
                                else:
                                    move = randint(1, 9)
                                    while str(move) not in board:
                                        move = randint(1, 9)
                                boardThisTurnHelp = board[:]
                                helpMoves.append(buttonsGame[int(move) - 1])

                else:
                    bIndex = getButtonIndex(buttonsPA, clickPos)
                    if bIndex != -1:
                        players = [['X', []], ['O', []]]
                        board = ['1', '2', '3',
                                 '4', '5', '6',
                                 '7', '8', '9']
                        added = False
                        helpMoves = []
                        if bIndex == 1:
                            userWins, AIWins, draws = 0, 0, 0
                            currentScreen = START_SCREEN
            elif currentScreen == AIDEFENCE_SCREEN:
                if checkWinner() is None:
                    bIndex = getButtonIndex(buttonsGame, clickPos)
                    if bIndex != -1:
                        if yourMove:
                            if bIndex != 9:
                                if str(bIndex + 1) in board:
                                    board[bIndex] = players[0][0]
                                    players[0][1].append(str(bIndex + 1))
                                    yourMove = False
                                else:
                                    boardThisTurn = board[:]
                                    start_ticks = pygame.time.get_ticks()
                            else:
                                boardPos = 0
                                boardSaved = False
                                move = 10
                                for savedBoard in savedMoves[0]:
                                    if ''.join(board) == savedBoard[0]:
                                        boardPos = savedMoves[0].index(savedBoard)
                                        boardSaved = True
                                        break
                                if boardSaved:
                                    max = 0
                                    for j, num in enumerate(savedMoves[0][boardPos][1][2::2]):
                                        if num > max:
                                            max = num
                                            move = savedMoves[0][boardPos][1][1::2][j]
                                else:
                                    move = randint(1, 9)
                                    while str(move) not in board:
                                        move = randint(1, 9)
                                boardThisTurnHelp = board[:]
                                helpMoves.append(buttonsGame[int(move) - 1])
                else:
                    bIndex = getButtonIndex(buttonsPA, clickPos)
                    if bIndex != -1:
                        players = [['X', []], ['O', []]]
                        board = ['1', '2', '3',
                                 '4', '5', '6',
                                 '7', '8', '9']
                        added = False
                        helpMoves = []
                        yourMove = True
                        if bIndex == 1:
                            userWins, AIWins, draws = 0, 0, 0
                            currentScreen = START_SCREEN
            elif currentScreen == HELP_SCREEN:
                bIndex = getButtonIndex(buttonsHelp, clickPos)
                if bIndex != -1:
                    if bIndex == 0:
                        currentScreen = START_SCREEN
                    elif bIndex == 1:
                        webbrowser.open('https://www.exploratorium.edu/brain_explorer/tictactoe.html')
    if currentScreen == SIM_SCREEN:
        AISimulation()
        players = [['X', []], ['O', []]]
        board = ['1', '2', '3',
                 '4', '5', '6',
                 '7', '8', '9']
        gamesSimulated += 1
    elif currentScreen == AIOFFENCE_SCREEN or currentScreen == AIDEFENCE_SCREEN:
        if checkWinner():
            if not added:
                if checkWinner() == 'draw':
                    draws += 1
                elif currentScreen == AIOFFENCE_SCREEN:
                    if checkWinner() == 'X':
                        mixer.stop()
                        mixer.Sound.play(lossSound)
                        AIWins += 1
                    elif checkWinner() == 'O':
                        mixer.stop()
                        mixer.Sound.play(winSound)
                        userWins += 1
                elif currentScreen == AIDEFENCE_SCREEN:
                    if checkWinner() == 'X':
                        mixer.stop()
                        mixer.Sound.play(winSound)
                        userWins += 1
                    elif checkWinner() == 'O':
                        mixer.stop()
                        mixer.Sound.play(lossSound)
                        AIWins += 1
                added = True
                yourMove = False
        elif not yourMove:
            if currentScreen == AIOFFENCE_SCREEN:
                boardPos = 0
                boardSaved = False
                move = 10
                for savedBoard in savedMoves[0]:
                    if ''.join(board) == savedBoard[0]:
                        boardPos = savedMoves[0].index(savedBoard)
                        boardSaved = True
                        break
                if boardSaved:
                    max = 0
                    for j, num in enumerate(savedMoves[0][boardPos][1][2::2]):
                        if num > max:
                            max = num
                            move = savedMoves[0][boardPos][1][1::2][j]
                else:
                    move = randint(1, 9)
                    while str(move) not in board:
                        move = randint(1, 9)
                board[int(move) - 1] = players[0][0]
                players[0][1].append(str(move))
                yourMove = True
            elif currentScreen == AIDEFENCE_SCREEN:
                boardPos = 0
                boardSaved = False
                move = 10
                for savedBoard in savedMoves[1]:
                    if ''.join(board) == savedBoard[0]:
                        boardPos = savedMoves[1].index(savedBoard)
                        boardSaved = True
                        break
                if boardSaved:
                    max = 0
                    for j, num in enumerate(savedMoves[1][boardPos][1][2::2]):
                        if num > max:
                            max = num
                            move = savedMoves[1][boardPos][1][1::2][j]
                else:
                    move = randint(1, 9)
                    while str(move) not in board:
                        move = randint(1, 9)
                board[int(move) - 1] = players[1][0]
                players[1][1].append(str(move))
                yourMove = True
