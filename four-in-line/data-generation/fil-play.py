from predict import Predict
from os import write
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
        print(c, r, '-')
        return True
    #Check verical line
    if LineCheck(board, _player, c, r, 1, 0) >= 4:
        print(c, r, '|')
        return True
    #Check diagonal line
    if LineCheck(board, _player, c, r, 1, 1) >= 4:
        print(c, r, '/')
        return True
    #Check couter diagonal line
    if LineCheck(board, _player, c, r, -1, 1) >= 4:
        print(c, r, '\\')
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

def AIChoice(board_now):
    possible_choices = []
    for i in range(7):
        if(len(board_now[i]) < 6):
            possible_choices.append(i)
    if len(possible_choices) == 0:
        print('dead game')
        return -1
    bestSoFar = possible_choices[0]
    bestPoints = 0
    for i in possible_choices:
        iChoice = copy.deepcopy(board_now)
        iChoice[i].append(0) #AI is always CPU that is always 0
        iPoints = Predict(iChoice)
        if iPoints > bestPoints:
            bestPoints = iPoints
            bestSoFar = i
    print('CPU move:', bestSoFar)
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

def Game():
    game_output = []
    board = [[], [], [], [], [], [], []]
    player = random.randint(0, 1)
    while True:
        printBoard(board)
        player = (player + 1) % 2
        if player == 0:
            print('CPU turn')
            n = AIChoice(board)
        else:
            n = int(input('What is your move?'))
        if n < 0:
            game_output = []
            board = [[], [], [], [], [], [], []]
            continue
        board[n].append(player)
        game_output.append((BoardToString(board), player))
        if WinningCheck(board, player, n):
            printBoard(board)
            playerName = 'CPU' if player == 0 else 'Player'
            print(playerName, 'wins!')
            break
    return (player, game_output)

######Start Here
print('Output file name:')
output_file = input() + '.txt'
print('Number of games:')
no_games = int(input())

i = 0
while(i < no_games):
    player, game_output = Game()
    WriteToFile(output_file, player, game_output)
    i = i + 1