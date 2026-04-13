import time
import random
import re
import os
import threading
from colorama import Fore, init


def verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado):
    for coords in statusCoordenadasNavios.values():
        if coords and all(tabuleiroAtacado[c[0]][c[1]] == "X" for c in coords):
            return True
    return False


def criaMesa(n1):
    tabuleiro = [[" " for _ in range(n1 + 1)] for _ in range(n1 + 1)]
    for i in range(1, n1 + 1):
        tabuleiro[0][i] = letras[i]
    for i in range(1, n1 + 1):
        tabuleiro[i][0] = str(i)
    for i in range(1, n1 + 1):
        for j in range(1, n1 + 1):
            tabuleiro[i][j] = "~"
    return tabuleiro


def printaMatriz(tabuleiro):
    for i in range(len(tabuleiro)):
        print("\t", end=" ")
        for j in range(len(tabuleiro[i])):
            if i != 0 and j != 0:
                if tabuleiro[i][j] == "~":
                    print(f"{color['blue']}{tabuleiro[i][j]:3}{color['reset']}", end=" ")
                elif tabuleiro[i][j] == "X":
                    print(f"{color['red']}{tabuleiro[i][j]:3}{color['reset']}", end=" ")
                elif tabuleiro[i][j] == "O":
                    print(f"{color['yellow']}{tabuleiro[i][j]:3}{color['reset']}", end=" ")
                elif tabuleiro[i][j] == "N":
                    print(f"{color['green']}{tabuleiro[i][j]:3}{color['reset']}", end=" ")
                else:
                    print(f"{tabuleiro[i][j]:3}", end=" ")
            else:
                print(f"{tabuleiro[i][j]:3}", end=" ")
        print()


def insereNavios(jogador, tabuleiro, tamanhoNavio, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios):
    colocouNavios = False
    while not colocouNavios:
        try:
            print(f"           Tabuleiro do {jogador}")
            printaMatriz(tabuleiro)
            print()
            print(f"As coordenadas que você colocar serão a {color['yellow']}ponta esquerda{color['reset']} do navio. O resto dele será {color['yellow']}colocado abaixo ou à direita{color['reset']} dessa coordenada.")
            match = None

            while match is None:
                coordenadaNavio = input(f"insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do {nomeNavio}: ").upper().replace(" ", "")
                match = re.match(r"(\d+)([A-Z]+)", coordenadaNavio)

                if match is None:
                    print(f"{color['red']}Coordenada inválida,{color['reset']} Tente novamente!")
                    continue
                tempLinha = int(match.group(1))
                tempColuna = letras.index(match.group(2))
                if tempLinha > proporcao or tempColuna > proporcao:
                    print(f"{color['red']}Coordenadas fora do alcance do tabuleiro{color['reset']}, tente novamente!")
                    match = None
                else:
                    linha = int(match.group(1))
                    coluna = letras.index(match.group(2))

            direcao = ""
            while direcao not in ["H", "V"]:
                direcao = input(f"Insira{color['yellow']} V{color['reset']} para colocar o navio na vertical e {color['yellow']}H{color['reset']} para colocar na horizontal: ").upper().strip()

                if direcao not in ["H", "V"]:
                    print(f"{color['red']}Direção inválida,{color['reset']} Tente novamente!")

            if direcao == "H":
                if coluna + tamanhoNavio - 1 > proporcao:
                    print(f"{color['red']}O navio não cabe na horizontal,{color['reset']} Tente novamente!")
                    continue

                if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanhoNavio)):
                    print(f"{color['red']}Posição já ocupada,{color['reset']} Tente novamente!")
                    continue

                coords = []
                for i in range(tamanhoNavio):
                    tabuleiro[linha][coluna + i] = "N"
                    coords.append((linha, coluna + i))
                statusCoordenadasNavios[nomeNavio] = coords
                colocouNavios = True

            elif direcao == "V":
                if linha + tamanhoNavio - 1 > proporcao:
                    print(f"{color['red']}Navio não cabe na vertical,{color['reset']} Tente novamente!")
                    continue

                if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanhoNavio)):
                    print(f"{color['red']}Posição já ocupada,{color['reset']} Tente novamente!")
                    continue

                coords = []
                for i in range(tamanhoNavio):
                    tabuleiro[linha + i][coluna] = "N"
                    coords.append((linha + i, coluna))
                statusCoordenadasNavios[nomeNavio] = coords
                colocouNavios = True

        except (ValueError, IndexError):
            print(f"{color['red']}Coordenada inválida,{color['reset']} Tente novamente.")
            continue


def introducaoJogo():
    print("\n" + "=" * 50)
    print("🛳🌊 BEM-VINDO AO JOGO BATALHA NAVAL 🌊🛳")
    print("=" * 50)
    print()
    #time.sleep(1)
    print(f"\t{color['red']}ATENÇÃO{color['reset']}\n\tA letra {color['green']}[N]{color['reset']} representa as partes do navio que não foram atingidas \n\tA letra {color['red']}[X]{color['reset']} representa acertos nos navios\n\tA letra {color['yellow']}[O]{color['reset']} representa acertos na água")
    print()
    #time.sleep(4)
    print(f"\tIniciando a configuração dos navios:")
    print()
    #time.sleep(1)
    print(f"{color['green']}Navios{color['reset']}:\n\t1 porta-aviões {color['yellow']}(5 espaços){color['reset']}\n\t1 Encouraçado {color['yellow']} (4 espaços){color['reset']}\n\t2 Cruzador {color['yellow']}    (3 espaços){color['reset']}\n\t2 Submarino {color['yellow']}  (2 espaços){color['reset']}")
    print()


def insereNaviosIA(tabuleiro, tamanhoNavio, proporcao, nomeNavio, statusCoordenadasNavios):
    colocouNavios = False
    while not colocouNavios:
        linha = random.randint(1, proporcao)
        coluna = random.randint(1, proporcao)
        direcao = random.choice(["V", "H"])
        if direcao == "H":
            coords = []
            if coluna + tamanhoNavio - 1 > proporcao:
                continue

            if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanhoNavio)):
                continue

            for i in range(tamanhoNavio):
                tabuleiro[linha][coluna + i] = "N"
                coords.append((linha, coluna + i))
            statusCoordenadasNavios[nomeNavio] = coords
            colocouNavios = True

        elif direcao == "V":
            coords = []
            if linha + tamanhoNavio - 1 > proporcao:
                continue

            if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanhoNavio)):
                continue

            for i in range(tamanhoNavio):
                tabuleiro[linha + i][coluna] = "N"
                coords.append((linha + i, coluna))
            statusCoordenadasNavios[nomeNavio] = coords
            colocouNavios = True


def introducaoBatalha():
    print("\n" + "=" * 60)
    print("🚢  TODOS OS NAVIOS FORAM POSICIONADOS  🚢")
    print("=" * 60)
    #time.sleep(1.5)
    print("🌊💣💥    QUE COMECE A BATALHA!    💥💣🌊")
    print("=" * 60)
    #time.sleep(1.5)
    print("""
                    ===========
                     ))_))))_)
                      )))_))_)
                     ))_))_))
                    ========                    
             _________|||_____
    ---------\\_____________//---------
      ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
            ^^^^    ^^^^   ^^^   ^^
                  ^^^^   ^^^
    """)


def jogada(tabuleiro, tabuleiroAtaque, tabuleiroAtacado, jogadorAtacado, jogador, statusCoordenadasNavios, proporcao):
    print(f"           Tabuleiro com seus navios, comandante {jogador}")
    printaMatriz(tabuleiro)
    print(f"           Tabuleiro de ataque")
    printaMatriz(tabuleiroAtaque)
    print()
    print(f"\t{color['red']}ATENÇÃO{color['reset']}\n\tA letra {color['green']}N{color['reset']} representa as partes do navio que não foram atingidas \n\tA letra {color['red']}X{color['reset']} representa acertos nos navios\n\tA letra {color['yellow']}O{color['reset']} representa acertos na água")
    jogadorPlacar = ""
    linha = -1
    coluna = -1

    if modoJogo == "1":
        if tabuleiro == tabuleiroUm:
            jogadorPlacar = "jogadorUm"
        elif tabuleiro == tabuleiroDois:
            jogadorPlacar = "jogadorDois"
    match = None
    while match is None:
        coordenadaAtaque = input(f"Insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do seu ataque: ").upper().replace(" ", "")
        match = re.match(r"(\d+)([A-Z]+)", coordenadaAtaque)
        if match is None:
            print(f"{color['reset']}Coordenada inválida, Tente novamente!")
        else:
            tempLinha = int(match.group(1))
            if match.group(2) in letras:
                tempColuna = letras.index(match.group(2))
            else:
                print(f"{color['red']}Coordenadas fora do alcance do tabuleiro,{color['reset']} Tente novamente!")
                match = None
                continue
            if proporcao < tempLinha or proporcao < tempColuna:
                print(f"{color['red']}Coordenadas fora do alcance do tabuleiro,{color['reset']} Tente novamente!")
                match = None
            else:
                linha = int(match.group(1))
                coluna = letras.index(match.group(2))

    if tabuleiroAtacado[linha][coluna] == "~":
        tabuleiroAtaque[linha][coluna] = "O"
        tabuleiroAtacado[linha][coluna] = "O"
        if modoJogo == "1":
            placar[jogadorPlacar]["tiros"] += 1
        elif modoJogo == "2":
            placarIA["jogadorUm"]["tiros"] += 1
    elif tabuleiroAtacado[linha][coluna] == "N":
        tabuleiroAtaque[linha][coluna] = "X"
        tabuleiroAtacado[linha][coluna] = "X"
        if modoJogo == "2":
            placarIA["jogadorUm"]["acertos"] += 1
            placarIA["jogadorUm"]["tiros"] += 1
        elif modoJogo == "1":
            placar[jogadorPlacar]["tiros"] += 1
            placar[jogadorPlacar]["acertos"] += 1
    else:
        print(f"{color['red']}Voce atirou duas vezes no mesmo lugar,{color['reset']} Cuidado!")
        if modoJogo == "1":
            placar[jogadorPlacar]["tiros"] += 1
        elif modoJogo == "2":
            placarIA["jogadorUm"]["tiros"] += 1
        #time.sleep(2)

    naviosInimigos = ["Porta-aviões", "Encouraçado", "CruzadorUm", "CruzadorDois", "SubmarinoUm", "SubmarinoDois"]
    naviosAfundadosContador = 0
    if modoJogo == "1":
        for nomeDoNavio in naviosInimigos:
            if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado):
                naviosAfundadosContador += 1
        placar[jogadorPlacar]["navios_abatidos"] = naviosAfundadosContador
    if modoJogo == "2":
        for nomeDoNavio in naviosInimigos:
            if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado):
                naviosAfundadosContador += 1
        placarIA["jogadorUm"]["navios_abatidos"] = naviosAfundadosContador

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"           Tabuleiro de ataque do comandante {jogador}")
    printaMatriz(tabuleiroAtaque)
    print(f"\tEssa foi sua jogada, {jogador}. Passe a vez para o outro jogador!")
    #time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')

    if not any("N" in linha for linha in tabuleiroAtacado):
        #time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Voce acabou com o {jogadorAtacado}!")
        print(f"Vitoria de {jogador}!!!")
        return True
    return False


def verificarCoordenadasLista(listaCoordenadas, proporcao):
    for i in range(len(listaCoordenadas) - 1, -1, -1):
        if (listaCoordenadas[i][0] > proporcao or listaCoordenadas[i][0] < 1 or
                listaCoordenadas[i][1] > proporcao or listaCoordenadas[i][1] < 1):
            listaCoordenadas.pop(i)
    return listaCoordenadas


def verificarSentidoBarco(coordenada_primeiro_acerto, coordenada_segundo_acerto, proporcao,sentido=""):
    coordenada_guia_caca = [[]]

    if coordenada_primeiro_acerto[0] > coordenada_segundo_acerto[0] and (sentido == "" or sentido == "N"):
        sentido = "N"
        coordenada_guia_caca = [
            [coordenada_segundo_acerto[0] - 1, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] - 2, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] - 3, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] - 4, coordenada_segundo_acerto[1]],
        ]
        coordenada_guia_caca = verificarCoordenadasLista(coordenada_guia_caca, proporcao)

        if coordenada_guia_caca == [[]]:
            sentido = "S"
            verificarSentidoBarco(coordenada_primeiro_acerto, coordenada_segundo_acerto, sentido)

    elif coordenada_primeiro_acerto[0] < coordenada_segundo_acerto[0] and (sentido == "" or sentido == "S"):
        sentido = "S"
        coordenada_guia_caca = [
            [coordenada_segundo_acerto[0] + 1, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] + 2, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] + 3, coordenada_segundo_acerto[1]],
            [coordenada_segundo_acerto[0] + 4, coordenada_segundo_acerto[1]],
        ]
        coordenada_guia_caca = verificarCoordenadasLista(coordenada_guia_caca, proporcao)

        if coordenada_guia_caca == [[]]:
            sentido = "N"
            verificarSentidoBarco(coordenada_primeiro_acerto, coordenada_segundo_acerto, sentido)

    if coordenada_primeiro_acerto[1] > coordenada_segundo_acerto[1] and (sentido == "" or sentido == "O"):
        sentido = "O"
        coordenada_guia_caca = [
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] - 1],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] - 2],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] - 3],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] - 4],
        ]
        coordenada_guia_caca = verificarCoordenadasLista(coordenada_guia_caca, proporcao)

        if coordenada_guia_caca == [[]]:
            sentido = "L"
            verificarSentidoBarco(coordenada_primeiro_acerto, coordenada_segundo_acerto, sentido)

    elif coordenada_primeiro_acerto[1] < coordenada_segundo_acerto[1] and (sentido == "" or sentido == "L"):
        sentido = "L"
        coordenada_guia_caca = [
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] + 1],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] + 2],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] + 3],
            [coordenada_segundo_acerto[0], coordenada_segundo_acerto[1] + 4],
        ]
        coordenada_guia_caca = verificarCoordenadasLista(coordenada_guia_caca, proporcao)

        if coordenada_guia_caca == [[]]:
            sentido = "O"
            verificarSentidoBarco(coordenada_primeiro_acerto, coordenada_segundo_acerto, sentido)

    return coordenada_guia_caca


def jogadaIAComEspera(tabuleiroAtaque, tabuleiroAtacado, coordenadasAtacadas, proporcao, statusCoordenadasNavios):
    pararEvento = threading.Event()
    threadLoading = threading.Thread(target=telaJogadorContraIA, args=(pararEvento, "esperando a IA fazer seu ataque"))
    threadLoading.start()

    acerto_aleatorio = getattr(jogadaIAComEspera, 'acerto_aleatorio', None)
    acerto_busca = getattr(jogadaIAComEspera, 'acerto_busca', None)
    modo_atual = getattr(jogadaIAComEspera, 'modo_atual', 'aleatorio')
    proximo_ataque = getattr(jogadaIAComEspera, 'proximo_ataque', [[]])

    modos_ataque = ["aleatorio", "busca", "caça"]

    linhaEscolhida = 0
    colunaEscolhida = 0
    atacou = False

    while not atacou:
        if modo_atual == "aleatorio":
            linhaEscolhida = random.randint(1, proporcao)
            colunaEscolhida = random.randint(1, proporcao)

        elif modo_atual in ["busca", "caça"]:
            if not proximo_ataque or proximo_ataque == [[]]:
                modo_atual = "aleatorio"
                jogadaIAComEspera.modo_atual = modo_atual
                continue
            linhaEscolhida = proximo_ataque[0][0]
            colunaEscolhida = proximo_ataque[0][1]

            if (linhaEscolhida, colunaEscolhida) in coordenadasAtacadas:
                proximo_ataque.pop(0)
                continue

        if (linhaEscolhida, colunaEscolhida) not in coordenadasAtacadas:
            coordenadasAtacadas.add((linhaEscolhida, colunaEscolhida))
            atacou = True

    celula = tabuleiroAtacado[linhaEscolhida][colunaEscolhida]
    if celula == "N":
        tabuleiroAtaque[linhaEscolhida][colunaEscolhida] = "X"
        tabuleiroAtacado[linhaEscolhida][colunaEscolhida] = "X"
        placarIA["IA"]["tiros"] += 1
        placarIA["IA"]["acertos"] += 1

        if modo_atual == "aleatorio":
            acerto_aleatorio = [linhaEscolhida, colunaEscolhida]
            modo_atual = "busca"
            proximo_ataque = [
                [linhaEscolhida + 1, colunaEscolhida],
                [linhaEscolhida - 1, colunaEscolhida],
                [linhaEscolhida, colunaEscolhida + 1],
                [linhaEscolhida, colunaEscolhida - 1]
            ]
            proximo_ataque = verificarCoordenadasLista(proximo_ataque, proporcao)

        elif modo_atual == "busca":
            acerto_busca = [linhaEscolhida, colunaEscolhida]
            if not verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado):
                modo_atual = "caça"
                proximo_ataque = verificarSentidoBarco(acerto_aleatorio, acerto_busca, proporcao)
                proximo_ataque = [c for c in proximo_ataque if (c[0], c[1]) not in coordenadasAtacadas]
            else:
                modo_atual = modos_ataque[0]

        elif modo_atual == "caça":
            if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado):
                modo_atual = "aleatorio"
                acerto_aleatorio = None
                acerto_busca = None
            else:
                proximo_ataque.pop(0)

    elif celula == "~":
        tabuleiroAtaque[linhaEscolhida][colunaEscolhida] = "O"
        tabuleiroAtacado[linhaEscolhida][colunaEscolhida] = "O"
        placarIA["IA"]["tiros"] += 1

        if modo_atual == "busca":
            proximo_ataque.pop(0)

        elif modo_atual == "caça":
            if acerto_aleatorio and acerto_busca:
                proximo_ataque = verificarSentidoBarco(acerto_busca, acerto_aleatorio, proporcao)
                proximo_ataque = [c for c in proximo_ataque if (c[0], c[1]) not in coordenadasAtacadas]
                if not proximo_ataque or proximo_ataque == [[]]:
                    modo_atual = "aleatorio"
                else:
                    modo_atual = "caça"

    jogadaIAComEspera.acerto_aleatorio = acerto_aleatorio
    jogadaIAComEspera.acerto_busca = acerto_busca
    jogadaIAComEspera.modo_atual = modo_atual
    jogadaIAComEspera.proximo_ataque = proximo_ataque


    if verificarNavioAbatido(statusCoordenadasNaviosDois, tabuleiroAtacado):
        placarIA["IA"]["navios_abatidos"] += 1


    #time.sleep(1.5)
    pararEvento.set()
    threadLoading.join()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"           seu tabuleiro após o ataque")
    printaMatriz(tabuleiroAtacado)
    print(f"A IA fez sua jogada!")
    #time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    if not any("N" in linha for linha in tabuleiroAtacado):
        #time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"A IA acabou com você!")
        print(f"Vitoria da IA!!!")
        return True
    return False


def telaJogadorContraIA(pararEvento, frase):
    pontos = [".", "..", "..."]
    while not pararEvento.is_set():
        for i in pontos:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{frase}{i}")
            #time.sleep(0.25)


def print_prosicionamento_navios(tabuleiro, jogador):
    print()
    printaMatriz(tabuleiro)
    print()
    print(f"\t Seu posicionamento final! 👆👆")
    #time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Configurações dos navios de {jogador} foram salvas!")
    #time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')


init()
color = {
    'blue': Fore.BLUE,
    'green': Fore.GREEN,
    'red': Fore.RED,
    'yellow': Fore.YELLOW,
    'reset': Fore.RESET
}

letras = [" "] + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
letrasDois = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
linha = 0
coluna = 0
proporcao = 0
continuar = ""
jogadorUm = ""
jogadorDois = ""
usernameUm = ""
usernameDois = ""
portaAvioes = 5
encouracado = 4
cruzador = 3
submarino = 2

modoJogo = input(f"Insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

while modoJogo != "1" and modoJogo != "2":
    print(f"{color['red']}Erro, tente novamente!{color['reset']} Dessa vez tente usar, apenas 1 ou 2 para seguir com as escolhas.")
    modoJogo = input(f"insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

if modoJogo == "1":
    while (usernameDois or usernameUm) == "":
        usernameUm = input("Jogador 1, insira seu nome: ")
        usernameDois = input("Jogador 2, insira seu nome: ")
        if (usernameDois or usernameUm) == "":
            print("Erro: Você deve inserir um username para cada jogador!")
            continue
        jogadorUm = usernameUm
        jogadorDois = usernameDois

elif modoJogo == "2":
    while usernameUm == "":
        usernameUm = input("Insira seu username: ")
        if usernameUm == "":
            print("Erro: Você deve inserir um username!")
            continue

        jogadorUm = usernameUm

    usernameDois = "IA"
    jogadorDois = usernameDois

proporcao = 0
while proporcao == 0:
    try:
        proporcaoTemp = int(input("Insira o numero que voce quer usar de prorporção para o tabuleiro: "))
        if proporcaoTemp < 5:
            print(f"{color['red']}Proporção deve ser no mínimo 5,{color['reset']} tente novamente!")
        if proporcaoTemp >= 5:
            proporcao = proporcaoTemp
    except Exception:
        print(f"{color['red']}A proporção deve ser numérica,{color['reset']} tente novamente!")

if proporcao > 26:
    letrasTemp = []
    for i in letrasDois:
        for j in letras:
            letrasTemp.append(f"{i}{j}")
    letras.extend(letrasTemp)

while continuar != "X":
    fim = False
    coordenadasAtacadas = set()

    navios_name_size = [
        ["Porta-aviões", 5], ["Encouraçado", 4], ["CruzadorUm", 3], ["CruzadorDois", 3], ["SubmarinoUm", 2], ["SubmarinoDois", 2]
    ]

    statusCoordenadasNaviosUm = {
        "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],
        "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
    }

    statusCoordenadasNaviosDois = {
        "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],
        "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
    }

    placar = {"jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0},
              "jogadorDois": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}}

    placarIA = {"jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0},
                "IA": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}}

    tabuleiroUm = criaMesa(proporcao)
    tabuleiroDois = criaMesa(proporcao)
    tabuleiroAtaqueUm = criaMesa(proporcao)
    tabuleiroAtaqueDois = criaMesa(proporcao)
    introducaoJogo()

    for i in range(len(statusCoordenadasNaviosUm)):
        insereNavios(jogadorUm, tabuleiroUm, navios_name_size[i][1], navios_name_size[i][0], proporcao, linha, coluna, statusCoordenadasNaviosUm)

    print_prosicionamento_navios(tabuleiroUm, jogadorUm)

    if usernameDois == "IA":
        for i in range(len(statusCoordenadasNaviosDois)):
            insereNaviosIA(tabuleiroDois, navios_name_size[i][1], proporcao, navios_name_size[i][0], statusCoordenadasNaviosDois)
    else:
        introducaoJogo()
        for i in range(len(statusCoordenadasNaviosDois)):
            insereNavios(jogadorDois, tabuleiroDois, navios_name_size[i][1], navios_name_size[i][0], proporcao, linha, coluna, statusCoordenadasNaviosDois)

        print_prosicionamento_navios(tabuleiroDois, jogadorDois)

    introducaoBatalha()

    while not fim:
        if usernameDois == "IA":
            fim = jogada(tabuleiroUm, tabuleiroAtaqueUm, tabuleiroDois, jogadorDois, jogadorUm, statusCoordenadasNaviosDois, proporcao)
            if not fim:
                fim = jogadaIAComEspera(tabuleiroAtaqueDois, tabuleiroUm, coordenadasAtacadas, proporcao,
                                        statusCoordenadasNaviosUm)
        else:
            fim = jogada(tabuleiroUm, tabuleiroAtaqueUm, tabuleiroDois, jogadorDois, jogadorUm, statusCoordenadasNaviosDois, proporcao)
            if not fim:
                fim = jogada(tabuleiroDois, tabuleiroAtaqueDois, tabuleiroUm, jogadorUm, jogadorDois, statusCoordenadasNaviosUm, proporcao)

    print("-" * 20, "Placar final", "-" * 20)
    if modoJogo == "1":
        print(f"Comandante {jogadorUm}:\n\tTiros: {placar['jogadorUm']['tiros']}\n\tAcertos: {placar['jogadorUm']['acertos']}\n\tNavios abatidos: {placar['jogadorUm']['navios_abatidos']}")
        print(f"Comandante {jogadorDois}:\n\tTiros: {placar['jogadorDois']['tiros']}\n\tAcertos: {placar['jogadorDois']['acertos']}\n\tNavios abatidos: {placar['jogadorDois']['navios_abatidos']}")
    else:
        print(f"Comandante {jogadorUm}:\n\tTiros: {placarIA['jogadorUm']['tiros']}\n\tAcertos: {placarIA['jogadorUm']['acertos']}\n\tNavios abatidos: {placarIA['jogadorUm']['navios_abatidos']}")
        print(f"IA:\n\tTiros: {placarIA['IA']['tiros']}\n\tAcertos: {placarIA['IA']['acertos']}\n\tNavios abatidos: {placarIA['IA']['navios_abatidos']}")

    continuar = input(f"pressione{color['yellow']} [ENTER] {color['reset']}para jogar mais uma e insira {color['yellow']}[X]{color['reset']} para parar de jogar: ").upper()