import pygame, sys
import pygame.locals

WIDTH = 500
HIGHT = 500

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


class PongGame(object):
    def __init__(self,width, height):
        pygame.init()

        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Pong Game!")

        pygame.mixer.music.load('MBG.wav')
        pygame.mixer.music.play(-1, 0.0)
        bg = pygame.image.load("background.jpg")

        self.fps_clock = pygame.time.Clock()

        self.pileczka = Pileczka(30, 30 ,width/2,height/2)
        self.player1 = Rakieta(100,20,width/2-50,450,(255,0,0))
        self.player2 = Rakieta(100,20,width/2-50,50,(0,0,255))
        self.komputer = Komputer(self.player2, self.pileczka)
        self.sedzia = Sedzia( self.pileczka, self.player2, self.pileczka)
        self.screen.fill((0, 0, 0))
        self.screen.blit(bg, (0, 0))
        self.pileczka.ruch(self.player1, self.player2)
        self.pileczka.draw_on(self.screen)
        self.player1.draw_on(self.screen)
        self.player2.draw_on(self.screen)
        self.sedzia.draw_on(self.screen)
        pygame.display.update()
        wait()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_a]:
                self.player1.ruc(-1)
            if keys[pygame.K_d]:
                self.player1.ruc(1)

            self.screen.fill((0,0,0))
            self.screen.blit(bg, (0,0))
            self.pileczka.ruch(self.player1,self.player2)
            self.pileczka.draw_on(self.screen)
            self.player1.draw_on(self.screen)
            self.player2.draw_on(self.screen)
            self.sedzia.draw_on(self.screen)

            pygame.display.update()
            self.fps_clock.tick(60)
            self.komputer.ruch()


class Przedmioty(object):
    def __init__(self,szerokosc, wysokosc, x, y,kolor=(0, 0, 100)):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.kolor = kolor
        self.surface = pygame.Surface([self.szerokosc, self.wysokosc], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)

class Pileczka(Przedmioty):
    def __init__(self,szerokosc, wysokosc, x, y,kolor=(0, 0, 100)):
        super(Pileczka, self).__init__(szerokosc, wysokosc,x, y,kolor)

        self.predkoscX = 4
        self.predkoscY = 4
        pilka = pygame.image.load("ball.png")
        self.surface.blit(pilka, (0, 0))
        pygame.display.update()

    def odwrocY(self):
        self.predkoscY *= -1

    def odwrocX(self):
        self.predkoscX *= -1

    def reset(self):
        self.rect.x = 250
        self.rect.y = 250

        self.odwrocY()
        wait()

    def ruch(self, *args):
        self.rect.x += self.predkoscX
        self.rect.y += self.predkoscY

        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.odwrocX()

        if self.rect.y < 0 or self.rect.y > HIGHT:
            self.odwrocY()

        for rakieta in args:
            if self.rect.colliderect(rakieta.rect):
                if self.rect.y  > rakieta.rect.y  or self.rect.y  < rakieta.rect.y :
                    self.odwrocY()

class Rakieta(Przedmioty):
    def __init__(self,szerokosc, wysokosc,x,y,kolor):
        super(Rakieta, self).__init__(szerokosc, wysokosc,x, y,kolor)

        self.maxPredkosc = 5
        self.surface.fill(self.kolor)
    def ruc(self,x):
        if self.rect.x > 0 and self.rect.x < self.x * 2 :
            self.rect.x += self.maxPredkosc * x
        elif self.rect.x > 0:
            if x == 1:
                pass
            else:
                self.rect.x += self.maxPredkosc * x
        else :
            if x == 1:
                self.rect.x += self.maxPredkosc * x
            else:
                pass

    def ruch(self, x):
        delta = x - self.rect.x

        if abs(delta) > self.maxPredkosc:
            delta = self.maxPredkosc if delta > 0 else -self.maxPredkosc
        self.rect.x += delta


class Komputer(object):
    def __init__(self,rakieta,pileczka):
        self.pileczka = pileczka
        self.rakieta = rakieta

    def ruch(self):
        x = self.pileczka.rect.centerx
        self.rakieta.ruch(x)

class Sedzia(object):
    def __init__(self, pilka, *args):
        self.pilka = pilka
        self.rakieta = args
        self.wynik = [0, 0]
        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 64)

    def aktualizujWynik(self, board_height):
        if self.pilka.rect.y < 15:
            self.wynik[0] += 1
            self.pilka.reset()
        elif self.pilka.rect.y > board_height-30:
            self.wynik[1] += 1
            self.pilka.reset()

    def napiszTekst(self, surface,  text, x, y):
        text = self.font.render(text, True, (150, 150, 150))
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)

    def draw_on(self, surface):
        height = HIGHT
        self.aktualizujWynik(height)
        width = WIDTH

        self.napiszTekst(surface, "Gracz: {}".format(self.wynik[0]), width/2, height * 0.3)
        self.napiszTekst(surface, "Komputer: {}".format(self.wynik[1]), width/2, height * 0.7)

if __name__ == '__main__':
    PongGame(WIDTH,HIGHT)