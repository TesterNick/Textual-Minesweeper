#!/usr/bin/env python3

"""
This is textual version of popular game Minesweeper.
Now you can play the game on your job even if sysadmins deleted all the games before you got your computer :)
If you find some typos or bugs please don't hesitate to report them.
"""
import random
import math


# There you can change game parameters such as game field width or height or how many bombs there are
easy = {
        "rows": 10,
        "columns": 10,
        "bombs_available": 15
    }
medium = {
        "rows": 15,
        "columns": 15,
        "bombs_available": 40
    }
hard = {
        "rows": 20,
        "columns": 20,
        "bombs_available": 80
    }
expert = {
        "rows": 26,
        "columns": 26,
        "bombs_available": 160
    }


# Names for columns. There are just 26 names for columns. If you need more, don't hesitate to add it here.
# Note: users_input function automatically switches the input to lowercase, so if English alphabet is not enough
# for you, try to expand it with 2-signs names (such as aa, ab and so on)
vertical_coordinates = " a b c d e f g h i j k l m n o p q r s t u v w x y z"
Russian = {
           "already_marked": "Вы уже отметили эту клетку как бомбу!"
                             "Если вы так больше не думаете, пожалуйста снимите метку!",
           "already_opened": "Эта клетка была открыта ранее! Попробуйте другую!",
           "bombs": "Осталось {} бомб",
           "choose_level": "Пожалуйста выберите уровень сложности:\n"
                           "1 - легкий, 2 - средний, 3 - сложный, 4 - эксперт.\n"
                           "Если нужна помощь, помните, вы всегда можете получить ее введя ?:\n",
           "error": "Что-то пошло не так! Отрицательное число бомб! ",
           "help_level": "В игре 4 уровня сложности. Они отличаются размером игрового поля и\n"
                         "количеством бомб на нем.\n"
                         "Легкий: поле 10х10, 15 бомб\n"
                         "Средний: поле 15х15, 40 бомб\n"
                         "Сложный: поле 20х20, 80 бомб\n"
                         "Эксперт: поле 26х26, 160 бомб\n",
           "help_game": "Со всех сторон игрового поля указаны координаты. Столбцы обозначены\n"
                        "английскими буквами,строки - арабскими цифрами. Таким образом, координаты\n"
                        "клетки - это комбинация имени столбца и номера строки, на пересечении\n"
                        "которых клетка находится. Букву и цифру можно вводить в любом порядке.\n"
                        "Также не имеет значения, заглавную или строчную букву вы введете. Главное -\n"
                        "убедитесь, что у вас включена английская раскладка на клавиатуре.\n"
                        "Для того, чтобы клетку открыть просто наберите соответствующие координаты,\n"
                        "чтобы отметить ее как имеющую бомбу, добавьте к ним восклицательный знак (!)\n"
                        "А сейчас нажмите Enter, чтобы вернуться к игре.",
           "luck": "Повезло!",
           "mistake": "Ошибочка вышла",
           "repeat": "Сыграем еще разок?\n1 - с теми же параметрами, 2 - изменить параметры, все остальное - выход:\n",
           "rip": "Пусть земля вам будет пухом...",
           "too_much": "Нельзя отметить бомбами больше клеток, чем бомб на поле!",
           "users_turn": "Введите координаты клетки, которую вы хотите открыть (х) или отметить (х!): ",
           "won": "Поздравляем! Вы выиграли!",
           "wrong_input": "Пожалуйста введите правильные координаты. Символы могут идти в любом порядке."
    }
English = {
           "already_marked": "You've already marked this cell as a bomb! "
                             "If you don't think so anymore, take off the mark! ",
           "already_opened": "This cell is already opened! Please try another one! ",
           "bombs": "There are {} bombs",
           "choose_level": "Please choose the difficulty: 1 - easy, 2 - medium, 3 - hard, 4 - expert.\n"
                           "If you need help, you always can input ?:\n",
           "error": "Something went wrong! There are negative number of bombs! ",
           "help_level": "There are 4 difficulty levels. They have different size of the game field\n"
                         "and different amount of bombs on it.\n"
                         "Easy: field 10x10, 15 bombs\n"
                         "Medium: field 15x15, 40 bombs\n"
                         "Hard: field 20x20, 80 bombs\n"
                         "Expert: field 26x26, 160 bombs\n",
           "help_game": "There are letters and numbers around the game field. Letters represents\n"
                        "column names and numbers - row names. Every cell is located on the\n"
                        "intersection of a row and a column. The names of the row and the column\n"
                        "combined make the cell's coordinates. You can input the letter and\n"
                        "the number in any order. Also, input is case-insensitive.\n"
                        "If you want to open a cell, just type it's coordinates. If you need to mark\n"
                        "the cell as a bomb, add an exclamation mark (!) to the coordinates.\n"
                        "Press Enter key to return to the game.",
           "luck": "You are lucky!",
           "mistake": "There's a mistake...",
           "repeat": "Would you like to play one more time?\n1 - yes, 2 - change settings, anything else - exit:\n",
           "rip": "Rest in peace...",
           "too_much": "You can't mark as bombs more cells than there are bombs! ",
           "users_turn": "Please enter coordinates of the cell you want to open (x) or mark (x!): ",
           "won": "Congratulations! You won! ",
           "wrong_input": "Please enter valid coordinates. Order of the symbols doesn't matter."
    }


# Languages. At the moment only Russian and English are supported
def choose_language():
    lang = None
    while lang is None:
        try:
            x = int(input("Пожалуйста выберите язык / Please choose your language\n"
                          "1 - Русский, 2 - English\n"))
        except (ValueError, TypeError):
            continue
        if x == 1:
            lang = Russian
        elif x == 2:
            lang = English
    return lang


# Difficulty level. Parameters of each level can be adjusted higher
def choose_level():
    lvl = None
    while lvl is None:
        raw_input = input(output["choose_level"])
        if "?" in raw_input:
            print(output["help_level"])
            continue
        try:
            x = int(raw_input)
        except (ValueError, TypeError):
            continue
        if x == 1:
            lvl = easy
        elif x == 2:
            lvl = medium
        elif x == 3:
            lvl = hard
        elif x == 4:
            lvl = expert
    return lvl


# Pretty print for data array with coordinates.
def print_array(array):
    vcoord = "  " + avail_vert_coord
    print(vcoord)
    for i in range(level["rows"]):
        num = i + 1
        field_line = " ".join(array[i])
        print("{0:2} {1} {0:2}".format(num, field_line))
    print(vcoord)


# Counts bombs near the chosen cell. Returns the number of bombs.
def count_nearby_bombs(y, x):
    number = 0
    neighbours = get_neighbours(x, y)
    for n in neighbours:
        if cells[n[1]][n[0]] == "!":
            number += 1
    return number


# Finds neighboring cells. Cells that are outside of the game field are skipped as well as the chosen cell itself.
# Returns the list of lists of indices.
def get_neighbours(x, y):
    neighbours = []
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if (0 <= i < level["rows"]) and (0 <= j < level["columns"]):
                if not (i == y and j == x):
                    neighbours.append([j, i])
    return neighbours


# Checks if some neighbours should be automatically marked as bombs.
# Marks a neighbour as a bomb if it is really bomb and have no closed cells around.
def auto_mark_bomb(x, y):
    neighb = get_neighbours(x, y)
    # For each neighbour checks if it is a bomb and if it is not marked.
    for n in neighb:
        bomb = (cells[n[1]][n[0]] == "!" and users_cells[n[1]][n[0]] != "!")
        if bomb:
            # Checks cells around the neighbour and if it has closed cells that are not bombs returns False.
            around = get_neighbours(n[0], n[1])
            for cell in around:
                closed = (users_cells[cell[1]][cell[0]] == "#")
                bomb = (cells[cell[1]][cell[0]] == "!")
                if closed and not bomb:
                    return False
            users_cells[n[1]][n[0]] = "!"
            return True


# Validates users input. Accepts letter and number in any order. Returns the list of x, y, and mark.
# Mark shows if the cell should be opened or just marked as a bomb.
def users_input():
    while True:
        x = y = None
        inp = (input(output["users_turn"])).lower()
        if "?" in inp:
            return "?"
        mark = "!" in inp
        for letter in avail_vert_coord:
            if letter in inp:
                x = int((avail_vert_coord.index(letter) - 1) / 2)
        for num in range(level["rows"], 0, -1):
            if str(num) in inp:
                y = int(num) - 1
                break
        if x is None or y is None:
            print(output["wrong_input"])
            continue
        if users_cells[y][x] == "?" and not mark:
            print(output["already_marked"])
            continue
        elif users_cells[y][x] != "#" and users_cells[y][x] != "?":
            print(output["already_opened"])
            continue
        strike = [x, y, mark]
        return strike


# Marks cell as bomb or not. Doesn't allow to mark as bombs more cells
# than there are bombs on the whole field. Always returns True.
def mark_cell(x, y):
    if check_bombs() > 0 or users_cells[y][x] == "?":
        users_cells[y][x] = "#" if users_cells[y][x] == "?" else "?"
    else:
        print(output["too_much"])
    return True


# Checks if the cell is not a bomb, changes data in both arrays and returns the number of nearby bombs
def open_cell(x, y):
    if cells[y][x] == "!":
        print("Illegal open_cell() invocation")
        return None
    elif users_cells[y][x] == "#":
        num = str(count_nearby_bombs(y, x))
        users_cells[y][x] = num
        cells[y][x] = num
        return num
    else:
        return None


# Recursive function for opening all the neighboring "zeros"
def open_zeros(x, y):
    num = str(count_nearby_bombs(y, x))
    neighb = get_neighbours(x, y)
    if num == "0":
        for n in neighb:
            if users_cells[n[1]][n[0]] == "#":
                open_cell(n[0], n[1])
                if cells[n[1]][n[0]] == "0":
                    open_zeros(n[0], n[1])
    else:
        print("Illegal open_zeros() invocation")


# Opens cells and changes data arrays. Returns False if player died and True otherwise.
def check_cell(x, y):
    if cells[y][x] == "!":
        # Adds a cross on the user's death place.
        cells[y][x] = "X"
        print(output["rip"])
        return False
    else:
        num = open_cell(x, y)
        if num == "0":
            open_zeros(x, y)
        else:
            neighb = get_neighbours(x, y)
            for n in neighb:
                auto_mark_bomb(n[0], n[1])
        print(output["luck"])
        return True


# Counts how many bombs are left unmarked.
def check_bombs():
    number = 0
    for line in cells:
        number += line.count("!")
    for line in users_cells:
        number -= line.count("!")
        number -= line.count("?")
    return number


# Checks if user really won. Returns False if not all bombs are found or if some bombs are marked wrong.
def win():
    win = False
    if check_bombs() == 0:
        win = True
        for i in range(level["rows"]):
            for j in range(level["columns"]):
                if users_cells[i][j] == "!" or users_cells[i][j] == "?":
                    if cells[i][j] != "!":
                        cells[i][j] = "X"
                        win = False
    return win


# The variable initialized as 2 to ask user about language and difficulty right after the game run.
rep = "2"
# Game starts here. There is greater loop to restart the game without restarting the program.
while True:
    if rep == "2":
        output = choose_language()
        level = choose_level()
    # Initialisation of other variables
    bombs = 0
    avail_vert_coord = vertical_coordinates[:level["columns"] * 2]

    # Creation of the field with bombs
    cells = [[" " for x in range(level["columns"])] for y in range(level["rows"])]
    while bombs < level["bombs_available"]:
        i = int(math.floor(random.random() * level["rows"]))
        j = int(math.floor(random.random() * level["columns"]))
        if cells[i][j] != "!":
            cells[i][j] = "!"
            bombs += 1

    # Creation of the user's field
    users_cells = [["#" for x in range(level["columns"])] for y in range(level["rows"])]

    # Main game loop
    while bombs > 0:
        print_array(users_cells)
        x = users_input()
        if x == "?":
            input(output["help_game"])
            success = True
        elif x[2]:
            success = mark_cell(x[0], x[1])
        else:
            success = check_cell(x[0], x[1])
        bombs = check_bombs()
        print(output["bombs"].format(bombs))
        if not success:
            break

    if win():
        print(output["won"])
    # Just for self testing :)
    elif bombs < 0:
        print("{}({})".format(output["error"], bombs))
    elif bombs == 0:
        print(output["mistake"])

    print_array(cells)

    rep = input(output["repeat"])
    if rep != "1" and rep != "2":
        break
