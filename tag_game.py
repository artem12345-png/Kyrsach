import random

up = """+-----+-----+-----+-----+
|     |     |     |     |"""

mid = """|     |     |     |     |
+-----+-----+-----+-----+
|     |     |     |     |"""

bot = """|     |     |     |     |
+-----+-----+-----+-----+"""


def get_new_random():
    line = list(range(16))
    random.shuffle(line)
    return line


def print_board(new_game):
    print(up)
    for i in range(0, 16):
        if new_game[i] < 10:
            if new_game[i] == 0:
                print('| ', end='')
            else:
                print('| ' + str(new_game[i]) + ' ', end='')
        else:
            num = str(new_game[i])
            print('| ' + num[0] + ' ' + num[1] + ' ', end='')
        if i == 3 or i == 7 or i == 11:
            print('|')
            print(mid)
    print('|')
    print(bot)



