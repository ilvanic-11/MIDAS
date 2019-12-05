####AUTHOR:
#DK3250
####SOURCE:
#"https://www.dreamincode.net/forums/topic/
#400712-matrix-rain-a-walk-through-with-focus-on-class-objects/"

import os
os.environ['PYGAME_FREETYPE'] = '1'
import pygame, sys, random
import pygame.freetype
import time


import unicodedata




#1920
#1080
#screen = pygame.display.set_mode((X, Y))
    ###pygame.FULLSCREEN)



#symbulge = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@%&#%$€")



#big_rand = random.random()
#symbols = [chr(i) for i in range(0x1d100, 0x1d1e8 + 1)]
# #nymbals = [ord(i) for i in Cymbols]
#Symballs = list()
# for i in Cymbols:
#     try:
#         Symballs.append(unicodedata.name(chr(ord(i))))
#         print(unicodedata.name(chr(ord(i))))
#     except ValueError:
#         print(i)
# symbols = list()
# for i in Symballs:
#     try:
#         if len(unicodedata.lookup(str(i))) == 1:
#             symbols.append(unicodedata.lookup((str(i))))
#     except UnicodeError:
#         symbols.append("♫", "♪")

# bigballs= list()
# for i in Cymbols:
#     try:
#         bigballs.append(unicodedata.name(str(i)))
#     except ValueError:
#         print(i)
# symbols = list()
# for i in bigballs:
#     try:
#         symbols.append(unicodedata.lookup(str(i)))
#     except KeyError:
#         print(i)


  #Default 16
#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\Code200365k.ttf", SIZE)

#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\unifont_upper-12.0.01.ttf", SIZE)
#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\LeedsUni10-12-13.ttf", SIZE)
#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\Quivira.ttf", SIZE)
#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\unison.ttf", SIZE)
#font = pygame.font.Font(None, SIZE)
#font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\FreeSerif.ttf", SIZE)


#font = pygame.freetype.Font(r"C:\\WINDOWS\\Fonts\\ARIALN.TTF", SIZE)
#font = pygame.freetype.Font(r"C:\Anaconda3\Lib\site-packages\pygame\FreeSerif.ttf", SIZE)


BLACK = (0,0,0)
X = 1920
Y = 1080
symbols = list('♫ ♪ ♩ ♬ ♩ ♫ ♬ ♭ ♮ ♯ ♪')    #'𝆺𝅥'A # Bb C > 𝆺𝅥
symbolz = list(" ♫ Mu s i c o d e ♫ || ♪ M i d i A r t ♪ || ♬ 3 i d i A r t ♬ ")
SIZE = 18
row_height = SIZE * 0.6
row_width = SIZE
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X,Y)

class Column():
    def __init__(self, x, screen, font):
        self.screen = screen
        self.font = font
        self.x = x
        self.random = random.random()
        self.clear_and_restart(1000)
        self.a = 0
        self.add_new_symbol()

        #self.rantom

    def add_new_symbol(self):
        if 0 < self.y < Y:
            self.list.append(Symbol(self, self.a, self.screen, self.font))
        self.a += 1
        if self.a >= len(symbolz):
            self.a = 0
        self.y += row_height

    def clear_and_restart(self, start_pos=250):
        pygame.draw.rect(self.screen, BLACK, (self.x - row_width // 2, 0, row_width, Y), 0)
        self.list = []
        self.y = - random.randint(0, start_pos // row_height) * row_height
        self.fade_age = random.randint(20, 40)
        self.fade_speed = random.randint(2, 5)

        if self.random < 0.97:  # new in this version
            self.color = "blue"
        else:
            self.color = "green"
            #Symbol.symbol = symbolz

    def move(self):
        if self.list and self.list[-1].color == BLACK:
            self.clear_and_restart()
        self.add_new_symbol()

    def update(self):
        for symbol in self.list:
            symbol.update()


class Symbol():
    def __init__(self, column, a, screen, font):
        self.x = column.x
        self.y = column.y
        self.screen = screen
        self.font = font
        #self.plus = 0
        #self.rantom = big_rand
        # if Column.rantom > .9:
        self.symbol = random.choice(symbols)

        # to return normal, self.symbol = random.choice(symbols)
        # else:
        #self.symbol = symbolz
        # if self.rantom > .9:
        #     self.symbol = [i for i in symbolz]
        self.age = 0
        self.fade_age = column.fade_age
        self.fade_speed = column.fade_speed


        #self.color_function = self.green  # new in this version
        self.color_function = self.blue #My chiggy wiggy blue.
        if column.color == "green": #default: orange
            self.color_function = self.green  #default: orange
            self.symbol = (symbolz[a])


    def update(self):
        self.draw()
        self.age += 1

    def draw(self):
        self.color_function()

        self.surf = self.font.render(self.symbol, 1, self.color)
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.screen.blit(self.surf, self.rect)

    def green(self):  # new name in this version
        if self.age < 11:
            self.color = (225 - self.age * 22, 225 - 7 * self.age, 225 - self.age * 22)
        elif self.age > self.fade_age:
            self.color = (0, max(0, 155 - (self.age - self.fade_age) * self.fade_speed), 0)

    def orange(self):  # alternative color
        if self.age < 11:
            self.color = (225 - 8 * self.age, 225 - 16 * self.age, 225 - self.age * 22)
            #print(self.color)
        elif self.age > self.fade_age:
            self.color = (max(0, 155 - (self.age - self.fade_age) * self.fade_speed),
                          max(0, 75 - (self.age - self.fade_age) * self.fade_speed // 2), 0)
            #print(self.color)

    def blue(self):
        if self.age < 11:
            self.color = (225 - self.age * 22, 225 - self.age * 22, 225 - 7 * self.age)
        elif self.age > self.fade_age:
            self.color = (0, 0, max(0, 155 - (self.age - self.fade_age) * self.fade_speed))


def rain_execute():
    pygame.init()
    pygame.display.set_caption("Musical Matrix Rain")
    pygame.freetype.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    font = pygame.font.Font(r"C:\Anaconda3\Lib\site-packages\pygame\Code2003Miao.ttf", SIZE)

    col = []
    for i in range(1, X // SIZE):
        col.append(Column(i * row_width, screen, font))

    screen.fill(BLACK)
    pygame.time.set_timer(pygame.QUIT, 10000)

    while True:
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()
                return
        for c in col:
            c.move()
            c.update()
        pygame.time.wait(20)
        pygame.display.flip()
        #time.sleep(5)
        #pygame.display.toggle_fullscreen()



if __name__ == '__main__':
    rain_execute()