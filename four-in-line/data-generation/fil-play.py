from predict import Predict
from os import write
import os
import random
import copy

def printBoard(board):
    for r in range(5, -1, -1):
        line = '|'
        for c in range(7):
            token = Board(board, c, r)
            token = '@' if token == 0 else 'O' if token == 1 else ' '
            line = line + token + '|'
        print(line)

def Board(board, c, r):
    if(c >= 0 and c <= 6 and r >= 0 and len(board[c]) > r):
        return board[c][r]
    else:
        return 2

def WinningCheck(board, _player, c):
    #Get row
    r = len(board[c]) - 1
    #Check horizontal line
    if LineCheck(board, _player, c, r, 0, 1) >= 4:
        #print(c, r, '-')
        return True
    #Check verical line
    if LineCheck(board, _player, c, r, 1, 0) >= 4:
        #print(c, r, '|')
        return True
    #Check diagonal line
    if LineCheck(board, _player, c, r, 1, 1) >= 4:
        #print(c, r, '/')
        return True
    #Check couter diagonal line
    if LineCheck(board, _player, c, r, -1, 1) >= 4:
        #print(c, r, '\\')
        return True
    return False

def LineCheck(board, _player, c, r, _vDir, _hDir):
    n = 1
    #Checking forward
    n = n + TokenCheck(board, _player, c + _hDir, r + _vDir, _vDir, _hDir)
    #Checking backward
    n = n + TokenCheck(board, _player, c - _hDir, r - _vDir, -_vDir, -_hDir)
    return n
    
def TokenCheck(board, _player, c, r, _vDir, _hDir):
    if(Board(board, c, r) == _player):
        n = 1 + TokenCheck(board, _player, c + _hDir, r + _vDir, _vDir, _hDir)    
    else:
        n = 0
    return n

def RandomChoice(board_now):
    possible_choices = []
    for i in range(7):
        if(len(board_now[i]) < 6):
            possible_choices.append(i)
    if len(possible_choices) == 0:
        print('dead game')
        return -1
    n = random.choice(possible_choices)
    return n

def AIChoice(board_now, ai, opponent, showText):
    possible_choices = []
    for i in range(7):
        if(len(board_now[i]) < 6):
            possible_choices.append(i)
    if len(possible_choices) == 0:
        print('dead game')
        return -1
    bestSoFar = possible_choices[0]
    bestPoints = -2
    for i in possible_choices:
        iChoice = copy.deepcopy(board_now)
        # AI is player ai
        iChoice[i].append(ai) 
        # Check for winning chance 
        if WinningCheck(iChoice, ai, i):
            bestSoFar = i
            break
        # Check for opponent winning chance
        jChoice = copy.deepcopy(board_now)
        jChoice[i].append(opponent)
        if WinningCheck(jChoice, opponent, i):
            bestPoints = 2 # So this is the best choice unless we find a chance to win later
            bestSoFar = i
            continue
        # If none of the players have a chance to win, lets predict the best move
        iPoints = Predict(iChoice)
        # Check for opponent next turn
        if len(iChoice[i]) < 6:
            iChoice[i].append(opponent)
            if WinningCheck(iChoice, opponent, i):
                iPoints = iPoints - 1
        # Compare with previous best move
        if iPoints > bestPoints:
            bestPoints = iPoints
            bestSoFar = i
    if showText == 0: print('CPU move:', bestSoFar)
    return bestSoFar

def BoardToString(board_now):
    s = ''
    for column in board_now:
        for row in column:
            s = s + str(row) + ','
        for i in range(6 - len(column)):
            s = s + 'x,'
    return s

def WriteToFile(path, winner, game_output):
    # code: -1 opponent, 0 free space, 1 AI player
    with open(path, 'a') as file:
        for move in game_output:
            x = move[0]
            if move[1] == 1:
                #Just to make the move from player 0's perspective
                x = x.replace('1', '2')
                x = x.replace('0', '1')
                x = x.replace('2', '0')
            x = x.replace('1', '-1')
            x = x.replace('0', '1')
            x = x.replace('x', '0')
            if move[1] == winner:
                file.write(x + '1\n')
            else:
                file.write(x + '0\n')

def Game(opponent):
    game_output = []
    board = [[], [], [], [], [], [], []]
    player = random.randint(0, 1)
    while True:
        if opponent == 0: printBoard(board)
        player = (player + 1) % 2
        ## AI is always player 0
        if player == 0:
            if opponent == 0: print('CPU turn')
            n = AIChoice(board, 0, 1, opponent)
        # If the opponent is a human
        elif opponent == 0:
            n = int(input('What is your move?'))
        # If the opponent is an AI
        elif opponent == 1:
            n = AIChoice(board, 1, 0, opponent)
        # If the opponent is an randomCPU
        else:
            n = RandomChoice(board)
        if n < 0:
            game_output = []
            board = [[], [], [], [], [], [], []]
            continue
        board[n].append(player)
        game_output.append((BoardToString(board), player))
        if WinningCheck(board, player, n):
            if opponent == 0: printBoard(board)
            playerName = 'CPU' if player == 0 else 'Player'
            if opponent == 0: print(playerName, 'wins!')
            break
    return (player, game_output)

######Start Here
print('who is playing? (0 - player) (1 - ai) (2 - randomCPU)')
opponent = int(input())
print('Output file name:')
output_file = input() + '.txt'
print('Number of games:')
no_games = int(input())
clear = lambda: os.system('cls')
    
i = 0
while(i < no_games):
    clear()
    print('Game: ', i, '/', no_games)
    player, game_output = Game(opponent)
    WriteToFile(output_file, player, game_output)
    i = i + 1

print('Finished!, outputfile:', output_file)