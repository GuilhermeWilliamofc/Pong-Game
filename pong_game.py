import pygame
from emoji import emojize

pygame.init()
pygame.display.set_caption(emojize('Pong Game :ping_pong: By Gw'))
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
FPS = 40

toque = pygame.mixer.Sound('toque.mp3')
ponto = pygame.mixer.Sound('ponto.mp3')

fonte = pygame.font.Font('freesansbold.ttf', 20)

preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
amarelo = (255, 255, 0)
roxo = (160, 32, 240)

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.geekRect = pygame.Rect(posx, posy, width, height)

        self.geek = pygame.draw.rect(tela, self.color, self.geekRect)
 
    def display(self):
        self.geek = pygame.draw.rect(tela, self.color, self.geekRect)
 
    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac
 
        if self.posy <= 0:
            self.posy = 0

        elif self.posy + self.height >= altura:
            self.posy = altura-self.height
 
        self.geekRect = (self.posx, self.posy, self.width, self.height)
 
    def displayScore(self, text, score, x, y, color):
        text = fonte.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
 
        tela.blit(text, textRect)
 
    def getRect(self):
        return self.geekRect

 
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            tela, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1
 
    def display(self):
        self.ball = pygame.draw.circle(
            tela, self.color, (self.posx, self.posy), self.radius)
 
    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac
 
        if self.posy <= 0 or self.posy >= altura:
            self.yFac *= -1
 
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= largura and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
 
    def reset(self):
        self.posx = largura//2
        self.posy = altura//2
        self.xFac *= -1
        self.firstTime = 1
 
    def hit(self):
        self.xFac *= -1
        toque.play()
 
    def getRect(self):
        return self.ball
 
 
def main():
    running = True
 
    geek1 = Striker(20, 0, 10, 100, 10, vermelho)
    geek2 = Striker(largura-30, 0, 10, 100, 10, roxo)
    ball = Ball(largura//2, altura//2, 7, 7, branco)
 
    Jogadores = [geek1, geek2]
 
    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0
 
    while running:
        tela.fill(preto)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0
 
        for geek in Jogadores:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
 
        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()
 
        if point == -1:
            geek1Score += 1
            ponto.play()
        elif point == 1:
            geek2Score += 1
            ponto.play()
 
        if point:   
            ball.reset()
 
        geek1.display()
        geek2.display()
        ball.display()
 
        geek1.displayScore("Jogador 1: ", 
                           geek1Score, 100, 20, amarelo)
        geek2.displayScore("Jogador 2: ", 
                           geek2Score, altura+100, 20, amarelo)
 
        pygame.display.update()
        relogio.tick(FPS)     
 
 
if __name__ == "__main__":
    main()
    pygame.quit()