import pygame
from random import randint
pygame.init()

# tamanho_jogo: o tamanho do tabuleiro em pixels
# linhas: a quantidade n de casas no tabuleito nXn
# block_size: o tamanho do bloco em pixels
# largura e altura placar: são o tamanho em pixels do placar
# largura e altura tela: o tamanho total da tela do jogo em pixels
tamanho_jogo = 400
linhas = 20
block_size = tamanho_jogo // linhas

largura_placar = tamanho_jogo
altura_placar = 100

largura_tela = tamanho_jogo
altura_tela = tamanho_jogo + altura_placar

# A classe bloco vai servir para criarmos tanto as frutas quanto as cobras
class Bloco(object):

    #pos: posicão do bloco no tabuleiro
    #dirx e diry: direção no eixo x e y para onde o bloco está apontando
    def __init__(self, pos, color=(255, 0, 0), dirx=1, diry=0):
        self.pos = pos
        self.color = color
        self.dirx = dirx
        self.diry = diry

    #desenhar(): desenha o bloco na tela
    def desenhar(self):
        pos_x, pos_y = self.pos
        pygame.draw.rect(tela, self.color, (pos_x*block_size, pos_y*block_size, block_size, block_size))

    #mover(): incrementa a posição do bloco em uma unidade na direção de dirx e diry
    def mover(self):

        if self.pos[0] == 0 and self.dirx == -1:
            self.pos = (linhas-1, self.pos[1])

        elif self.pos[0] == linhas-1 and self.dirx == 1:
            self.pos = (0, self.pos[1])

        elif self.pos[1] == 0 and self.diry == -1:
            self.pos = (self.pos[0], linhas-1)

        elif self.pos[1] == linhas-1 and self.diry == 1:
            self.pos = (self.pos[0], 0)

        else:
            self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)


#A classe cobra consiste num conjunto de blocos
class Snake(object):

    #corpo armazena os blocos presentes no corpo da cobra
    #virou é um dicionario, onde as chaves são posições no tabuleiro e os valores são direções para onde a cobra virou
    #cabeca é o primeiro bloco no corpo da cobra
    #player armazena se a cobra pertence ao primeiro ou segundo jogador
    def __init__(self, pos=(0, 0), color=(0, 255, 0), player=1):
        self.corpo = []
        self.virou = {}
        self.color = color
        self.cabeca = Bloco(pos=pos, color=self.color)
        self.corpo.append(self.cabeca)
        self.cabeca.dirx = 1
        self.cabeca.diry = 0
        self.player = player

    #mover() verifica quais teclas foram pressionadas e muda a direção da cobra de acordo. Além disso, todos os blocos pertencentes ao corpo da cobra
    #que passarem por alguma posição presente em "virou", vai ter sua direção mudada de acordo com a direção setada para aquela posição
    def mover(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        teclas = pygame.key.get_pressed()

        if self.player == 1:
            if teclas[pygame.K_LEFT] and self.cabeca.dirx != 1:
                self.virou[self.cabeca.pos[:]] = (-1, 0)

            elif teclas[pygame.K_UP] and self.cabeca.diry != 1:
                self.virou[self.cabeca.pos[:]] = (0, -1)

            elif teclas[pygame.K_RIGHT] and self.cabeca.dirx != -1:
                self.virou[self.cabeca.pos[:]] = (1, 0)

            elif teclas[pygame.K_DOWN] and self.cabeca.diry != -1:
                self.virou[self.cabeca.pos[:]] = (0, 1)

        if self.player == 2:
            if teclas[pygame.K_a] and self.cabeca.dirx != 1:
                self.virou[self.cabeca.pos[:]] = (-1, 0)

            elif teclas[pygame.K_w] and self.cabeca.diry != 1:
                self.virou[self.cabeca.pos[:]] = (0, -1)

            elif teclas[pygame.K_d] and self.cabeca.dirx != -1:
                self.virou[self.cabeca.pos[:]] = (1, 0)

            elif teclas[pygame.K_s] and self.cabeca.diry != -1:
                self.virou[self.cabeca.pos[:]] = (0, 1)



        for numero_do_bloco, bloco_do_corpo in enumerate(self.corpo):

            if bloco_do_corpo.pos in self.virou.keys():
                bloco_do_corpo.dirx, bloco_do_corpo.diry = self.virou[bloco_do_corpo.pos]
                if numero_do_bloco == len(self.corpo)-1:
                    self.virou.pop(bloco_do_corpo.pos)

            bloco_do_corpo.mover()

    #chama o metodo desenhar() de Bloco para todos os blocos pertencentes ao corpo da cobra
    def desenhar(self):
        for parte_do_corpo in self.corpo:
            parte_do_corpo.desenhar()

    #verifica para que direção a calda da cobra está apontando, e adiciona um bloco à calda de acordo com essa informação
    def add_block(self):
        dir_x_calda = self.corpo[-1].dirx
        dir_y_calda = self.corpo[-1].diry

        if dir_x_calda == -1:
            self.corpo.append(Bloco(pos=(self.corpo[-1].pos[0] + 1, self.corpo[-1].pos[1]), color=self.color, dirx=dir_x_calda, diry=dir_y_calda))

        if dir_x_calda == 1:
            self.corpo.append(Bloco(pos=(self.corpo[-1].pos[0] - 1, self.corpo[-1].pos[1]), color=self.color, dirx=dir_x_calda, diry=dir_y_calda))

        if dir_y_calda == -1:
            self.corpo.append(Bloco(pos=(self.corpo[-1].pos[0], self.corpo[-1].pos[1] + 1), color=self.color, dirx=dir_x_calda, diry=dir_y_calda))

        if dir_y_calda == 1:
            self.corpo.append(Bloco(pos=(self.corpo[-1].pos[0], self.corpo[-1].pos[1] - 1), color=self.color, dirx=dir_x_calda, diry=dir_y_calda))

    #esvazia o corpo e a variavel virou da cobra, além de gerar uma nova cabeça para a cobra
    def kill_snake(self):
        self.corpo = []
        self.virou = {}
        if self.player == 1:
            self.cabeca = Bloco(pos=(0, 0), color=self.color)
        if self.player == 2:
            self.cabeca = Bloco(pos=(5, 5), color=self.color)
        self.corpo.append(self.cabeca)

#A classe Button serve para termos menus interativos no jogo
class Button(object):

    #image on e out são as imagens que serão mostradas dependendo se o mouse está sobre a imagem ou não
    #x e y são as coordenadas da posição do canto superior esquerdo do botão
    #mensagem é a mensagem que será exibida pelo botão
    def __init__(self, text, x, y, largura=100, altura=40):
        self.text = text

        self.image_mouse_out = pygame.Surface((largura, altura))
        self.image_mouse_out.fill((0, 255, 0))

        self.image_mouse_on = pygame.Surface((largura, altura))
        self.image_mouse_on.fill((255, 0, 0))

        self.image = self.image_mouse_out
        self.rect = self.image.get_rect()

        self.mensagem = font_menu.render(text, True, (255, 255, 255))
        self.rect_mensagem = self.mensagem.get_rect(center=self.rect.center)

        self.image_mouse_out.blit(self.mensagem, self.rect_mensagem)
        self.image_mouse_on.blit(self.mensagem, self.rect_mensagem)

        self.rect.topleft = (x, y)

    #confere se o mouse está sobre o botão e se ele foi clicado
    def atualizar(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_mouse_on
            if pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False
        else:
            self.image = self.image_mouse_out
            return False


    #desenha o botão
    def desenhar(self):
        tela.blit(self.image, self.rect)


#gera uma fruta numa posição aleatoria em que não haja uma cobra
def fruta_alearoia(number_players_selected, cobra, cobra2=None):
    pos_x = randint(0, linhas-1)
    pos_y = randint(0, linhas-1)

    if number_players_selected == 1:
        while len(list(filter(lambda x: x.pos == (pos_x, pos_y), cobra.corpo))) > 0:
            pos_x = randint(0, linhas-1)
            pos_y = randint(0, linhas-1)

    if number_players_selected == 2:
        while len(list(filter(lambda x: x.pos == (pos_x, pos_y), cobra.corpo))) > 0 or len(list(filter(lambda x: x.pos == (pos_x, pos_y), cobra2.corpo))) > 0:
            pos_x = randint(0, linhas-1)
            pos_y = randint(0, linhas-1)

    return Bloco(pos=(pos_x, pos_y))

#verifica se houve uma colisão entre a fruta e a cobra
def check_fruta(number_players, cobra1, fruta, pt1, pt2=0, cobra2=None):
    if number_players == 1:
        if cobra1.cabeca.pos == fruta.pos:
                fruta = fruta_alearoia(number_players, cobra)
                cobra.add_block()
                pt1 += 1

        return fruta, pt1

    if number_players == 2:
        if cobra1.cabeca.pos == fruta.pos:
                fruta = fruta_alearoia(number_players, cobra, cobra2=cobra2)
                cobra.add_block()
                pt1 += 1

        if cobra2.cabeca.pos == fruta.pos:
                fruta = fruta_alearoia(number_players, cobra, cobra2=cobra2)
                cobra2.add_block()
                pt2 += 1

        return fruta, pt1, pt2

#verifica se houve uma colisão entre as cobras
def check_colisao(number_players, cobra1, cobra2=None):

    if number_players == 1:
        if len(list(filter(lambda x: x.pos == cobra1.cabeca.pos, cobra1.corpo[1:]))) > 0:
            print('colisão')
            cobra1.kill_snake()
            return True

        return False

    if number_players == 2:
        if len(list(filter(lambda x: x.pos == cobra1.cabeca.pos, cobra1.corpo[1:]))) > 0:
            print('colisão')
            cobra1.kill_snake()
            cobra2.kill_snake()
            return True

        if len(list(filter(lambda x: x.pos == cobra2.cabeca.pos, cobra2.corpo[1:]))) > 0:
            print('colisão')
            cobra1.kill_snake()
            cobra2.kill_snake()
            return True

        return False


def desenhar_grade(tela):
    x = 0
    y = 0
    pygame.draw.line(tela, (0, 0, 0), (0, y), (tamanho_jogo, y))
    for linha in range(linhas):
        x = x + block_size
        y = y + block_size

        pygame.draw.line(tela, (0, 0, 0), (x, 0), (x, tamanho_jogo))
        pygame.draw.line(tela, (0, 0, 0), (0, y), (tamanho_jogo, y))


def desenhar_placar(tela, number_players_selected, pt1, pt2=0):
    if number_players_selected == 1:
        text = font_pt.render(str(pt1) + ' pts', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (largura_tela/2, largura_tela + altura_placar/2)
        tela.blit(text, textRect)

    if number_players_selected == 2:
        text1 = font_pt.render(str(pt1) + ' pts', True, (0, 255, 0))
        textRect1 = text1.get_rect()
        textRect1.center = (largura_tela/4, largura_tela + altura_placar/2)

        text2 = font_pt.render(str(pt2) + ' pts', True, (0, 0, 255))
        textRect2 = text2.get_rect()
        textRect2.center = (largura_tela/4 + largura_tela/2, largura_tela + altura_placar/2)

        tela.blit(text1, textRect1)
        tela.blit(text2, textRect2)


def desenhar_menu_inicial(tela):
    global one_player_selected, two_players_selected

    tela.fill((150, 150, 150))
    desenhar_grade(tela)

    text = font_menu.render('Selecione o Numero de Jogadores:', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = ((largura_tela/2), largura_tela + altura_placar/4)

    one_player.desenhar()
    one_player_selected = one_player.atualizar()

    two_players.desenhar()
    two_players_selected = two_players.atualizar()

    tela.blit(text, textRect)
    pygame.display.update()


def desenhar_death_screen(number_players_selected, pt1, tela, pt2=0):
    global jogar_novamente_selected, sair_selected

    tela.fill((150, 150, 150))
    desenhar_grade(tela)

    if number_players_selected == 1:
        text = font_menu.render('Fim de Jogo. Você fez ' + str(pt1) + 'pontos', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = ((largura_tela/2), largura_tela + altura_placar/4)

        jogar_novamente.desenhar()
        jogar_novamente_selected = jogar_novamente.atualizar()

        sair.desenhar()
        sair_selected = sair.atualizar()

        tela.blit(text, textRect)
        pygame.display.update()

    if number_players_selected == 2:
        text = font_menu.render('Fim de Jogo. jogador 1: ' + str(pt1) + 'pts. Jogador 2: ' + str(pt2) + ' pts', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = ((largura_tela/2), largura_tela + altura_placar/4)

        jogar_novamente.desenhar()
        jogar_novamente_selected = jogar_novamente.atualizar()

        sair.desenhar()
        sair_selected = sair.atualizar()

        tela.blit(text, textRect)
        pygame.display.update()


def desenhar_jogo(tela, number_players_selected, cobra1, cobra2=None):

    tela.fill((150, 150, 150))
    if number_players_selected == 1:
        cobra1.desenhar()
        desenhar_placar(tela, 1, pt1)

    if number_players_selected == 2:
        cobra1.desenhar()
        cobra2.desenhar()
        desenhar_placar(tela, 2, pt1, pt2=pt2)

    fruta.desenhar()
    desenhar_grade(tela)
    pygame.display.update()

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Cobrinha')
pygame.display.update()

font_pt = pygame.font.Font('freesansbold.ttf', 32)
font_menu = pygame.font.Font('freesansbold.ttf', 15)
pt1 = 0
pt2 = 0
number_players = 0
dead_snake = False

cobra = Snake(player=1)
cobra2 = Snake(pos=(5, 5), color=(0, 0, 255), player=2)
fruta = fruta_alearoia(1, cobra)

one_player = Button('Um Jogador', x=block_size, y=tamanho_jogo + altura_placar/2, largura=150)
two_players = Button('Dois Jogadores', x=10*block_size, y=tamanho_jogo + altura_placar/2, largura=150)
one_player_selected = False
two_players_selected = False

jogar_novamente = Button('Jogar Novamente', x=block_size, y=tamanho_jogo + altura_placar/2, largura=150)
sair = Button('Sair', x=10*block_size, y=tamanho_jogo + altura_placar/2, largura=150)
jogar_novamente_selected = False
sair_selected = False

clock = pygame.time.Clock()
while True:

    while True:
        pygame.time.delay(75)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        desenhar_menu_inicial(tela)
        if one_player_selected or two_players_selected:
            break

    if one_player_selected:
        number_players = 1
        while True:
            pygame.time.delay(75)
            clock.tick(30)
            cobra.mover()
            fruta, pt1 = check_fruta(number_players, cobra, fruta, pt1)
            dead_snake = check_colisao(number_players, cobra)
            desenhar_jogo(tela, number_players, cobra)
            if dead_snake:
                break

    if two_players_selected:
        number_players = 2
        while True:
            pygame.time.delay(75)
            clock.tick(30)
            cobra.mover()
            cobra2.mover()
            fruta, pt1, pt2 = check_fruta(number_players, cobra, fruta, pt1, cobra2=cobra2, pt2=pt2)
            dead_snake = check_colisao(number_players, cobra, cobra2=cobra2)
            desenhar_jogo(tela, number_players, cobra, cobra2=cobra2)
            if dead_snake:
                break


    if dead_snake:
        while True:
            pygame.time.delay(75)
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            desenhar_death_screen(number_players, pt1, tela, pt2=pt2)
            dead_snake = False
            if jogar_novamente_selected or sair_selected:
                pt1 = 0
                pt2 = 0
                break

    if sair_selected:
        pygame.quit()
