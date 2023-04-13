#hangman 10.2

import pygame as py
import nltk    #library for english dictionary
from nltk.corpus import brown   #importing standard english words
from sys import exit
from random import choice
import re #for finding the special character
from nltk.corpus import wordnet #for the word meaning 

#importing world length over 4 letters
words = [word for word in nltk.corpus.brown.words() if 4 < len(word) < 8]

#Size for the screen
WINS = [940, 650]

#initializing the pygame
py.init()
screen = py.display.set_mode(WINS)
py.display.set_caption("Hangman 10.2")
Clock = py.time.Clock()
screen.fill((111,169,196))

#Making Fonts
text_font = py.font.Font('resources/fonts/Pixeltype.ttf', 50)
win_font = py.font.Font(None, 60)
meaning_font = py.font.Font(None, 30)
dash_font = py.font.Font(None, 60)
display_font = py.font.Font('resources/fonts/Pixeltype.ttf', 50)

#importing Pictures
hangPics = []
for i in range(7):
    h = py.image.load(f"resources/hangmanpic/hangman{i}.png").convert_alpha()
    h = py.transform.rotozoom(h, 0, 1.5) #making the images larger
    hangPics.append(h)

#Making a word list 
letters = []
radius = 25
gap = 15
start_x = round((WINS[0] - (radius *2 + gap)*13) / 2)
start_y = 450
for i in range(26):
    x = start_x + gap*2 + ((radius * 2 + gap) * (i%13))
    y = start_y + ((i // 13) * (gap + radius * 2))
    letters.append([x, y, chr(65 + i), True])


class Meaning:
    def __init__(self,word) -> None:
        self.gs_word = word
        # print(word)
        self.meaning_list = wordnet.synsets(word)

        # print(self.meaning_list)
        self.definition = self.meaning_list[0].definition()
        # print(self.definition)
        if len(self.definition) > 95:
            match = re.search(r'[?|`~:;,123456789()]', self.definition)
            if match:  
                i = match.start()
            else:
                i = len(self.definition)
        else:
            i = len(self.definition)
        self.render_meaning = meaning_font.render(self.definition[:i:].capitalize(), False, 'Black')

    def meaningPage(self):
        
        screen.blit(self.render_meaning, (10,30))

    def meaning_for_developer(self):

        screen.blit(self.render_meaning, (10,90))
        

class Screen(Meaning):
    game_screen = {"open":True, "first":False, "win": False, "lost": False, "developer": False}
    def __init__(self, word) -> None:
        self.__guess_word = word
        self.Game_Activity = False
        self.right_choice = [None] * len(self.__guess_word)
        self.mistake = 0
        self.showMistake = 0
        self.render_word = win_font.render(self.__guess_word.upper(), False, 'blue')
        
        super().__init__(self.__guess_word)

        self.first_page = py.image.load("resources/pages/open_page.png").convert()
        self.lost = py.image.load("resources/pages/lost_page.png").convert()
        self.win = py.image.load("resources/pages/win_page.png").convert()


    def playAgain(self):
        self.win_lost_dev('first')
        for letter in letters:
            letter[3] = True
        play_again = Hangman()
        play_again.play()   

    def OPEN_SCREEN(self):

        screen.blit(hangPics[self.mistake], (100,70))

        #drawing the letters and the circle
        for letter in letters:
            x,y,ltr,visible = letter
            if visible:
                py.draw.circle(screen, 'Black', (x, y), radius, 3)
                text = display_font.render(ltr, 1, 'black')
                screen.blit(text, (x - text.get_width() /2  , (y - text.get_height()/2 ) + 3 )) 

    def win_lost_dev(self, do):
        for i in Screen.game_screen:
            if i == do:
                Screen.game_screen[i] = True    
            else:
                Screen.game_screen[i] = False

    def dash_and_word_print(self):
        self.display_word = " "
        check_word = ''
        # print(self.right_choice)
        for i in self.right_choice:
            if i != None:
                self.display_word += i.upper()+ " " 
                check_word += i.lower()
            else:
                self.display_word += "_ "  

        ltr = dash_font.render(self.display_word, False, "black")
        screen.blit(ltr, (550, 300))
        
        self.mistakePrint()

        if self.mistake >3:
            self.meaningPage()

        if check_word == self.__guess_word:
            self.win_lost_dev("win")

        if self.mistake == 6:
            self.win_lost_dev('lost')

    def mistakePrint(self):
        mis = display_font.render(f"Your Mistake: {str(self.showMistake)}", False, "brown")
        screen.blit(mis, (600,100))

    def lostPage(self):
        screen.blit(self.lost, (0,0))
        screen.blit(self.render_word, (470,400))
        for event in py.event.get():
            if event.type == py.QUIT:
                    py.quit()
                    exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.playAgain()
                
    def winPage(self):
        screen.blit(self.win, (0,0))
        screen.blit(self.render_word, (520, 348))
        for event in py.event.get():
            if event.type == py.QUIT:
                    py.quit()
                    exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.playAgain()  
                    
    def developerPage(self):
        cheat = win_font.render('This is a cheat for the developer', False, 'black')
        screen.fill('white')
        screen.blit(cheat, (0,0))
        screen.blit(self.render_word, (350,300))
        # notice = 'Welcome Sir Developer'
        # notice_render = win_font.render(notice, False, "black")
        # screen.blit(notice_render, (0,300))
        credit = 'Made by Hirok Roy Rahul'
        credit_render = win_font.render(credit, False, "black")
        screen.blit(credit_render, (300,550))

        self.meaning_for_developer()

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    self.win_lost_dev('first')

    def open_page(self):
        screen.blit(self.first_page, (0,0))
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.win_lost_dev("first")

class Hangman(Screen):
    def __init__(self) -> None:
        self.choseWords()
        super().__init__(self.__guess_word)
        self.mistake_list = []
       
    def choseWords(self):
        word = choice(words).lower()
        
        if len(wordnet.synsets(word)) == 0 or re.search(r'[?|`~:;,123456789()]', word): 
            self.choseWords()
        else:
            self.__guess_word = word

    def index(self, ltr):
        for i,j in enumerate(self.__guess_word):
            if j == ltr:
                self.right_choice[i] = j

    def hide(self,word):
        for letter in letters:
            x,y,ltr,visible = letter
            if word == ltr.lower():
                letter[3] = False   

    def two_mistake(self):
        self.mistake_list.append(1)
        self.showMistake +=1
        if len(self.mistake_list) == 2:
            self.mistake +=1
            self.mistake_list.clear()
            
    def play(self):

        # print(self.__guess_word) #Printing the Guess Word for developer
       
        while True :

            screen.fill((111,169,196)) # a great bug just 4 hours of my life :)

            if Screen.game_screen["open"]:
              self.open_page()

            elif Screen.game_screen["first"]:
                self.OPEN_SCREEN()
                self.dash_and_word_print()

            elif Screen.game_screen["win"]:
                self.winPage()
                
            elif Screen.game_screen["lost"]:
                self.lostPage()

            elif Screen.game_screen["developer"]:
                self.developerPage()

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        exit()
                    if py.key.name(event.key) in self.__guess_word:
                        self.index(py.key.name(event.key))
                        self.hide(py.key.name(event.key))

                    if py.key.name(event.key) not in self.__guess_word:
                        self.two_mistake()
                        self.hide(py.key.name(event.key))

                    if py.key.name(event.key) in "1":
                        self.win_lost_dev("developer")
                        
            py.display.update()
            Clock.tick(20)

if __name__ == "__main__":
    first_Player = Hangman()
    first_Player.play()
