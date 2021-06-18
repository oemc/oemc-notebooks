from os import write
import random

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

def BoardToString(board_now):
    s = ''
    for column in board_now:
        for row in column:
            s = s + str(row) + ','
        for i in range(6 - len(column)):
            s = s + 'x,'
    return s

def WriteToFile(path, winner, game_output):
    with open(path, 'a') as file:
        for move in game_output:
            x = move[0]
            if move[1] == 1:
                #Just to make the move from player 0's perspective
                x = x.replace('1', '2')
                x = x.replace('0', '1')
                x = x.replace('2', '0')
            if move[1] == winner:
                file.write(x + '1\n')
            else:
                file.write(x + '0\n')

def Game():
    game_output = []
    board = [[], [], [], [], [], [], []]
    player = 0
    while True:
        player = (player + 1) % 2
        n = RandomChoice(board)
        if n < 0:
            game_output = []
            board = [[], [], [], [], [], [], []]
            continue
        board[n].append(player)
        game_output.append((BoardToString(board), player))
        if WinningCheck(board, player, n):
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