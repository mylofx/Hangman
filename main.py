import sqlite3
from sqlite3 import Error
import random

try:
    conn = sqlite3.connect('words.s3db')
except Error as e:
    print(e)
cur = conn.cursor()

try:
    cur.execute('CREATE TABLE words(word text, category text)')
except:
    pass
conn.commit()

all_words = []


cur.execute("SELECT * From words")
all_words = cur.fetchall()
print(all_words)
def print_all_words():
    xx = 0
    for lol in range(len(all_words)):
        xd = all_words[xx]
        print('Słowo: {} || Kategoria: {}'.format(xd[0], xd[1]))
        xx += 1

def random_word():
    index_w = random.randint(0, len(all_words) - 1)
    return all_words[index_w]

def hangman(word, category):

    wrong = 0
    stages = ["",
              "__________",
              "|               ",
              "|          |    ",
              "|          0    ",
              "|         /|\   ",
              "|         / \   ",
              "|               "
              ]
    rletters = list(word)
    board = ['_'] * len(word)
    win = False

    while wrong < len(stages) - 1:
        print('')
        print('Kategoria: {}                                  Wpisz "0" żeby się poddać'.format(category,))
        print('')
        print(board)
        print("""
        Odgadnij litere: """)
        char = input()
        bad = True
        for i in rletters:
            try:
                cind = rletters.index(char)
                board[cind] = char
                rletters[cind] = '$'
                bad = False
            except:
                pass

        if char == '0':
            break
        if len(char) > 1:
            if char == word:
                print('Wygrałeś!')
                win = True
                break

        if bad:
            wrong += 1
            e = wrong + 1
            print('\n'.join(stages[0:e]))
            bad = False
        else:
            e = wrong + 1
            print('\n'.join(stages[0:e]))
        if '_' not in board:
            print('Wygrałeś!')
            win = True
            break
    if not win:
        print('\n'.join(stages[0:wrong]))
        print('Przegrałeś! Miałeś odgadnąc "{}"'.format(word))

def menu():
    print('')
    print("GRA w WISIELCA!")
    print("")
    print("""1.Graj
2. dodaj słowo
3. wyświetl liste słów
0. wyjscie""")
    x = input()
    if x == '1':
        w_c = random_word()
        hangman(w_c[0], w_c[1])
    elif x == '0':
        exit()
    elif x == '2':
        słowo_dodaj = input("Wpisz słowo: ")
        kategoria_dodaj = input('Wpisz kategorie:')
        try:
            cur.execute("SELECT word From words where word = ?", (słowo_dodaj,))
        except:
            cur.execute('insert into words (word, category) values (?,?)', (słowo_dodaj, kategoria_dodaj))
            conn.commit()
            cur.execute("SELECT * From words")
            all_words = cur.fetchall()

    elif x == '3':
        print_all_words()
while True:
    menu()