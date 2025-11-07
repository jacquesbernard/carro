# ===============================================
# JOGO DE CORRIDA ASCII - VERSÃO ORIGINAL
# Autor: Jacques Bernard (2025)
# Linguagem: Python 3
# -----------------------------------------------
# Conceito: O jogador controla um carro em uma
# estrada gerada proceduralmente. O cenário rola,
# aparecem obstáculos, e o placar aumenta.
# ===============================================

import os
import time
import random
import sys
import shutil
import threading

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import termios, tty, select

# ----------------------------------------------------
# Classe utilitária para capturar as teclas em tempo real
# ----------------------------------------------------
class Teclado:
    def __init__(self):
        self.tecla = None
        self.ativo = True
        self.thread = threading.Thread(target=self._escutar, daemon=True)
        self.thread.start()

    def _escutar(self):
        if IS_WINDOWS:
            while self.ativo:
                if msvcrt.kbhit():
                    self.tecla = msvcrt.getwch()
        else:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            while self.ativo:
                dr, _, _ = select.select([sys.stdin], [], [], 0)
                if dr:
                    self.tecla = sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def ler(self):
        t = self.tecla
        self.tecla = None
        return t

    def parar(self):
        self.ativo = False


# ----------------------------------------------------
# Classe principal do jogo de corrida em ASCII
# ----------------------------------------------------
class CorridaASCII:
    def __init__(self):
        self.cols, self.rows = shutil.get_terminal_size(fallback=(80, 24))
        self.largura_estrada = 30
        self.posicao = self.largura_estrada // 2
        self.velocidade = 0.05
        self.pontuacao = 0
        self.vidas = 3
        self.obstaculos = []
        self.tempo_inicio = time.time()
        self.jogando = True
        self.teclado = Teclado()

    def limpar_tela(self):
        os.system('cls' if IS_WINDOWS else 'clear')

    def gerar_estrada(self):
        # Retorna uma linha ASCII representando a estrada
        margem = (self.cols - self.largura_estrada) // 2
        esquerda = "|"
        direita = "|"
        interior = [" " for _ in range(self.largura_estrada - 2)]

        # Adiciona obstáculo aleatório
        if random.random() < 0.15:
            pos_obs = random.randint(1, self.largura_estrada - 3)
            interior[pos_obs] = "X"
            self.obstaculos.append(pos_obs)

        return " " * margem + esquerda + "".join(interior) + direita

    def desenhar_carro(self, linha, pos):
        # Desenha o carro do jogador (A)
        margem = (self.cols - self.largura_estrada) // 2
        l = list(linha)
        x = margem + pos
        if 0 <= x < len(l):
            l[x] = "A"
        return "".join(l)

    def atualizar(self):
        tecla = self.teclado.ler()
        if tecla:
            if tecla in ['a', 'A', '\x1b[D']:
                self.posicao -= 1
            elif tecla in ['d', 'D', '\x1b[C']:
                self.posicao += 1
            elif tecla in ['q', 'Q']:
                self.jogando = False

        self.posicao = max(1, min(self.largura_estrada - 2, self.posicao))

    def loop_principal(self):
        estrada = [" " * self.cols for _ in range(self.rows - 5)]

        while self.jogando and self.vidas > 0:
            self.atualizar()
            nova = self.gerar_estrada()
            estrada.append(nova)
            if len(estrada) > self.rows - 5:
                estrada.pop(0)

            # Verifica colisão
            if len(self.obstaculos) > 0:
                if random.random() < 0.25 and self.posicao in self.obstaculos:
                    self.vidas -= 1
                    self.obstaculos.clear()
                    if self.vidas <= 0:
                        break

            # Exibe na tela
            self.limpar_tela()
            print("╔" + "═" * (self.cols - 2) + "╗")
            print(f" Pontuação: {self.pontuacao:05d} | Vidas: {self.vidas} | Use 'A'/'D' para mover | 'Q' para sair ")
            print("╠" + "═" * (self.cols - 2) + "╣")

            for i, linha in enumerate(estrada):
                if i == len(estrada) - 2:
                    print(self.desenhar_carro(linha, self.posicao))
                else:
                    print(linha)

            print("╚" + "═" * (self.cols - 2) + "╝")

            self.pontuacao += 1
            time.sleep(self.velocidade)

        self.teclado.parar()
        self.fim_de_jogo()

    def fim_de_jogo(self):
        self.limpar_tela()
        print("\n" * (self.rows // 3))
        print(" " * ((self.cols // 2) - 10) + "💥 FIM DE JOGO 💥")
        print(" " * ((self.cols // 2) - 10) + f"Pontuação final: {self.pontuacao}")
        print(" " * ((self.cols // 2) - 10) + "Obrigado por jogar!\n")


# ----------------------------------------------------
# Execução do jogo
# ----------------------------------------------------
if __name__ == "__main__":
    jogo = CorridaASCII()
    jogo.loop_principal()
