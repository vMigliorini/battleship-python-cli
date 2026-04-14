import time
import random
import re
import os
import threading
from colorama import Fore, init


def verificar_navio_abatido(coords_navios, tabuleiro_atacado):
    for coords in coords_navios.values():
        if coords and all(tabuleiro_atacado[c[0]][c[1]] == "X" for c in coords):
            return True
    return False

def criar_tabuleiro(n1, letras):
    tabuleiro = [[" " for _ in range(n1 + 1)] for _ in range(n1 + 1)]
    for i in range(1, n1 + 1):
        tabuleiro[0][i] = letras[i]
    for i in range(1, n1 + 1):
        tabuleiro[i][0] = str(i)
    for i in range(1, n1 + 1):
        for j in range(1, n1 + 1):
            tabuleiro[i][j] = "~"
    return tabuleiro

def printar_tabuleiro(tabuleiro, color):
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

def validar_coordenada_insercao(color, letras, proporcao, nome_navio):
    match = None
    linha = 0
    coluna = 0

    while match is None:
        coordenada_navio = input(
            f"insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do {nome_navio}: ").upper().replace(
            " ", "")
        match = re.match(r"(\d+)([A-Z]+)", coordenada_navio)

        if match is None:
            print(f"{color['red']}Coordenada inválida,{color['reset']} Tente novamente!")
            continue
        linha_temp = int(match.group(1))
        coluna_temp = letras.index(match.group(2))
        if linha_temp > proporcao or coluna_temp > proporcao:
            print(f"{color['red']}Coordenadas fora do alcance do tabuleiro{color['reset']}, tente novamente!")
            match = None
        else:
            linha = int(match.group(1))
            coluna = letras.index(match.group(2))

    return linha, coluna

def validar_direcao(color):
    direcao = ""
    while direcao not in ["H", "V"]:
        direcao = input(
            f"Insira{color['yellow']} V{color['reset']} para colocar o navio na vertical e {color['yellow']}H{color['reset']} para colocar na horizontal: ").upper().strip()

        if direcao not in ["H", "V"]:
            print(f"{color['red']}Direção inválida,{color['reset']} Tente novamente!")
    return direcao

def verificar_disponibilidade_de_coords_horizontal(coluna, tamanho_navio, proporcao, color, tabuleiro, linha):
    if coluna + tamanho_navio - 1 > proporcao:
        print(f"{color['red']}O navio não cabe na horizontal,{color['reset']} Tente novamente!")
        return False

    if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanho_navio)):
        print(f"{color['red']}Posição já ocupada,{color['reset']} Tente novamente!")
        return False

    return True

def verificar_disponibilidade_de_coords_vertical(linha, tamanho_navio, proporcao, color, tabuleiro, coluna):
    if linha + tamanho_navio - 1 > proporcao:
        print(f"{color['red']}Navio não cabe na vertical,{color['reset']} Tente novamente!")
        return False

    if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanho_navio)):
        print(f"{color['red']}Posição já ocupada,{color['reset']} Tente novamente!")
        return False

    return True

def inserir_navios(linha, coluna, tamanho_navio, color, proporcao, tabuleiro, coords_navios, nome_navio):

    direcao = validar_direcao(color)

    if direcao == "H":

        disponivel = verificar_disponibilidade_de_coords_horizontal(coluna, tamanho_navio, proporcao, color, tabuleiro, linha)

        if not disponivel:
            return False

        coords = []
        for i in range(tamanho_navio):
            tabuleiro[linha][coluna + i] = "N"
            coords.append((linha, coluna + i))
        coords_navios[nome_navio] = coords
        return True

    elif direcao == "V":

        disponivel = verificar_disponibilidade_de_coords_vertical(linha, tamanho_navio, proporcao, color, tabuleiro, coluna)

        if not disponivel:
            return False

        coords = []
        for i in range(tamanho_navio):
            tabuleiro[linha + i][coluna] = "N"
            coords.append((linha + i, coluna))
        coords_navios[nome_navio] = coords
        return True


    return False

def posicionar_navios(jogador, tabuleiro, tamanho_navio, nome_navio, proporcao, coords_navios, letras, color):

    posicionou_navio = False
    while not posicionou_navio:
        try:

            print(f"           Tabuleiro do {jogador}")
            printar_tabuleiro(tabuleiro, color)
            print()
            print(f"As coordenadas que você colocar serão a {color['yellow']}ponta esquerda{color['reset']} do navio. O resto dele será {color['yellow']}colocado abaixo ou à direita{color['reset']} dessa coordenada.")

            coords_insercao_navios = validar_coordenada_insercao(color, letras, proporcao, nome_navio)
            linha = coords_insercao_navios[0]
            coluna = coords_insercao_navios[1]

            posicionou_navio = inserir_navios(linha, coluna, tamanho_navio, color, proporcao, tabuleiro, coords_navios, nome_navio)

        except (ValueError, IndexError):
            print(f"{color['red']}Coordenada inválida,{color['reset']} Tente novamente.")
            continue

def introducao_jogo(color):
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

def validar_coords_insercao_horizontal_ia(coluna, tamanho_navio, proporcao, tabuleiro, linha):
    if coluna + tamanho_navio - 1 > proporcao:
        return False

    if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanho_navio)):
        return False

    return True

def validar_coordes_insercao_vertical_ia(linha, tamanho_navio, proporcao, tabuleiro, coluna):
    if linha + tamanho_navio - 1 > proporcao:
        return False

    if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanho_navio)):
        return False

    return True

def aplicar_navios_horizontal_tabuleiro(tamanho_navio,tabuleiro, linha, coluna, coords, coords_navios, nome_navio):
    for i in range(tamanho_navio):
        tabuleiro[linha][coluna + i] = "N"
        coords.append((linha, coluna + i))
    coords_navios[nome_navio] = coords
    return True

def aplicar_navios_vertical_tabuleiro(tamanho_navio,tabuleiro, linha, coluna, coords, coords_navios, nome_navio):
    for i in range(tamanho_navio):
        tabuleiro[linha + i][coluna] = "N"
        coords.append((linha + i, coluna))
    coords_navios[nome_navio] = coords
    return True

def inserir_navios_ia(tabuleiro, tamanho_navio, proporcao, nome_navio, coords_navios):
    posicionou_navio = False
    while not posicionou_navio:
        linha = random.randint(1, proporcao)
        coluna = random.randint(1, proporcao)
        direcao = random.choice(["V", "H"])
        if direcao == "H":
            coords = []

            coordenadas_livres = validar_coords_insercao_horizontal_ia(coluna, tamanho_navio, proporcao, tabuleiro, linha)

            if not coordenadas_livres:
                continue

            posicionou_navio = aplicar_navios_horizontal_tabuleiro(tamanho_navio,tabuleiro, linha, coluna, coords, coords_navios, nome_navio)

        elif direcao == "V":
            coords = []

            coordenadas_livres = validar_coordes_insercao_vertical_ia(linha, tamanho_navio, proporcao, tabuleiro, coluna)
            if not coordenadas_livres:
                continue

            posicionou_navio = aplicar_navios_vertical_tabuleiro(tamanho_navio,tabuleiro, linha, coluna, coords, coords_navios, nome_navio)

def introducao_batalha():
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

def validar_coordenada(color, letras, proporcao):
    match = None
    linha_final = 0
    coluna_final = 0
    while match is None:
        coordenada_ataque = input(
            f"Insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do seu ataque: ").upper().replace(
            " ", "")
        match = re.match(r"(\d+)([A-Z]+)", coordenada_ataque)
        if match is None:
            print(f"{color['reset']}Coordenada inválida, Tente novamente!")
        else:
            linha_temp = int(match.group(1))
            if match.group(2) in letras:
                coluna_temp = letras.index(match.group(2))
            else:
                print(f"{color['red']}Coordenadas fora do alcance do tabuleiro,{color['reset']} Tente novamente!")
                match = None
                continue
            if proporcao < linha_temp or proporcao < coluna_temp:
                print(f"{color['red']}Coordenadas fora do alcance do tabuleiro,{color['reset']} Tente novamente!")
                match = None
            else:
                linha_final = int(match.group(1))
                coluna_final = letras.index(match.group(2))
    return linha_final, coluna_final

def atualizar_placar(coords_navios, tabuleiro_atacado, modo_jogo, placar, chave_placar, placar_ia):
    navios_afundados = sum(
        1 for coords in coords_navios.values()
        if coords and all(tabuleiro_atacado[c[0]][c[1]] == "X" for c in coords)
    )

    if modo_jogo == "1":
        placar[chave_placar]["navios_abatidos"] = navios_afundados
    elif modo_jogo == "2":
        placar_ia["jogadorUm"]["navios_abatidos"] = navios_afundados

def aplicar_tiro(tabuleiro_atacado, tabuleiro_ataque, linha, coluna, modo_jogo, placar, chave_placar, placar_ia, color):
    if tabuleiro_atacado[linha][coluna] == "~":
        tabuleiro_ataque[linha][coluna] = "O"
        tabuleiro_atacado[linha][coluna] = "O"
        if modo_jogo == "1":
            placar[chave_placar]["tiros"] += 1
        elif modo_jogo == "2":
            placar_ia["jogadorUm"]["tiros"] += 1
    elif tabuleiro_atacado[linha][coluna] == "N":
        tabuleiro_ataque[linha][coluna] = "X"
        tabuleiro_atacado[linha][coluna] = "X"
        if modo_jogo == "2":
            placar_ia["jogadorUm"]["acertos"] += 1
            placar_ia["jogadorUm"]["tiros"] += 1
        elif modo_jogo == "1":
            placar[chave_placar]["tiros"] += 1
            placar[chave_placar]["acertos"] += 1
    else:
        print(f"{color['red']}Voce atirou duas vezes no mesmo lugar,{color['reset']} Cuidado!")
        if modo_jogo == "1":
            placar[chave_placar]["tiros"] += 1
        elif modo_jogo == "2":
            placar_ia["jogadorUm"]["tiros"] += 1
        #time.sleep(2)

def verificar_fim_de_jogo(tabuleiro_atacado, jogador_atacado, jogador):
    if not any("N" in linha for linha in tabuleiro_atacado):
        #time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Voce acabou com o {jogador_atacado}!")
        print(f"Vitoria de {jogador}!!!")
        return True
    return False

def jogada(tabuleiro, tabuleiro_ataque, tabuleiro_atacado, jogador_atacado, coords_navios, proporcao, modo_jogo, placar_ia, letras, color, placar, jogador):
    print(f"           Tabuleiro com seus navios, comandante {jogador}")
    printar_tabuleiro(tabuleiro, color)
    print(f"           Tabuleiro de ataque")
    printar_tabuleiro(tabuleiro_ataque, color)
    print()
    print(f"\t{color['red']}ATENÇÃO{color['reset']}\n\tA letra {color['green']}N{color['reset']} representa as partes do navio que não foram atingidas \n\tA letra {color['red']}X{color['reset']} representa acertos nos navios\n\tA letra {color['yellow']}O{color['reset']} representa acertos na água")


    chave_placar = jogador

    tupla_coordenadas = validar_coordenada(color, letras, proporcao)

    linha = tupla_coordenadas[0]
    coluna = tupla_coordenadas[1]

    aplicar_tiro(tabuleiro_atacado, tabuleiro_ataque, linha, coluna, modo_jogo, placar, chave_placar, placar_ia, color)

    atualizar_placar(coords_navios, tabuleiro_atacado, modo_jogo, placar, chave_placar, placar_ia)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"           Tabuleiro de ataque do comandante {jogador}")
    printar_tabuleiro(tabuleiro_ataque, color)
    print(f"\tEssa foi sua jogada, {jogador}. Passe a vez para o outro jogador!")
    #time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')

    fim = verificar_fim_de_jogo(tabuleiro_atacado, jogador_atacado, jogador)

    if fim:
        return True
    return False

def filtrar_coordenadas_validas(lista_coordenadas, proporcao):
    for i in range(len(lista_coordenadas) - 1, -1, -1):
        if (lista_coordenadas[i][0] > proporcao or lista_coordenadas[i][0] < 1 or
                lista_coordenadas[i][1] > proporcao or lista_coordenadas[i][1] < 1):
            lista_coordenadas.pop(i)
    return lista_coordenadas

def calcular_proximos_ataques(primeiro_acerto, segundo_acerto, proporcao, sentido=""):
    proximos_ataques = [[]]

    if primeiro_acerto[0] > segundo_acerto[0] and (sentido == "" or sentido == "N"):
        sentido = "N"
        proximos_ataques = [
            [segundo_acerto[0] - 1, segundo_acerto[1]],
            [segundo_acerto[0] - 2, segundo_acerto[1]],
            [segundo_acerto[0] - 3, segundo_acerto[1]],
            [segundo_acerto[0] - 4, segundo_acerto[1]],
        ]
        proximos_ataques = filtrar_coordenadas_validas(proximos_ataques, proporcao)

        if proximos_ataques == [[]]:
            sentido = "S"
            calcular_proximos_ataques(primeiro_acerto, segundo_acerto, sentido)

    elif primeiro_acerto[0] < segundo_acerto[0] and (sentido == "" or sentido == "S"):
        sentido = "S"
        proximos_ataques = [
            [segundo_acerto[0] + 1, segundo_acerto[1]],
            [segundo_acerto[0] + 2, segundo_acerto[1]],
            [segundo_acerto[0] + 3, segundo_acerto[1]],
            [segundo_acerto[0] + 4, segundo_acerto[1]],
        ]
        proximos_ataques = filtrar_coordenadas_validas(proximos_ataques, proporcao)

        if proximos_ataques == [[]]:
            sentido = "N"
            calcular_proximos_ataques(primeiro_acerto, segundo_acerto, sentido)

    if primeiro_acerto[1] > segundo_acerto[1] and (sentido == "" or sentido == "O"):
        sentido = "O"
        proximos_ataques = [
            [segundo_acerto[0], segundo_acerto[1] - 1],
            [segundo_acerto[0], segundo_acerto[1] - 2],
            [segundo_acerto[0], segundo_acerto[1] - 3],
            [segundo_acerto[0], segundo_acerto[1] - 4],
        ]
        proximos_ataques = filtrar_coordenadas_validas(proximos_ataques, proporcao)

        if proximos_ataques == [[]]:
            sentido = "L"
            calcular_proximos_ataques(primeiro_acerto, segundo_acerto, sentido)

    elif primeiro_acerto[1] < segundo_acerto[1] and (sentido == "" or sentido == "L"):
        sentido = "L"
        proximos_ataques = [
            [segundo_acerto[0], segundo_acerto[1] + 1],
            [segundo_acerto[0], segundo_acerto[1] + 2],
            [segundo_acerto[0], segundo_acerto[1] + 3],
            [segundo_acerto[0], segundo_acerto[1] + 4],
        ]
        proximos_ataques = filtrar_coordenadas_validas(proximos_ataques, proporcao)

        if proximos_ataques == [[]]:
            sentido = "O"
            calcular_proximos_ataques(primeiro_acerto, segundo_acerto, sentido)

    return proximos_ataques

def escolher_coords_ataque_ia(modo_atual, proporcao, proximo_ataque, coordenadas_atacadas):
    linha_escolhida = 0
    coluna_escolhida = 0
    atacou = False

    while not atacou:
        if modo_atual == "aleatorio":
            linha_escolhida = random.randint(1, proporcao)
            coluna_escolhida = random.randint(1, proporcao)

        elif modo_atual in ["busca", "caça"]:
            if not proximo_ataque or proximo_ataque == [[]]:
                modo_atual = "aleatorio"
                jogada_ia.modo_atual = modo_atual
                continue
            linha_escolhida = proximo_ataque[0][0]
            coluna_escolhida = proximo_ataque[0][1]

            if (linha_escolhida, coluna_escolhida) in coordenadas_atacadas:
                proximo_ataque.pop(0)
                continue

        if (linha_escolhida, coluna_escolhida) not in coordenadas_atacadas:
            coordenadas_atacadas.add((linha_escolhida, coluna_escolhida))
            atacou = True

    return linha_escolhida, coluna_escolhida

def aplicar_tiro_ia(modo_atual, proximo_ataque, modos_ataque, coordenadas_atacadas, coords_navios, acerto_aleatorio, proporcao, acerto_busca, tabuleiro_atacado, linha_escolhida, coluna_escolhida, tabuleiro_ataque, placar_ia):
    celula = tabuleiro_atacado[linha_escolhida][coluna_escolhida]
    if celula == "N":
        tabuleiro_ataque[linha_escolhida][coluna_escolhida] = "X"
        tabuleiro_atacado[linha_escolhida][coluna_escolhida] = "X"
        placar_ia["IA"]["tiros"] += 1
        placar_ia["IA"]["acertos"] += 1

        if modo_atual == "aleatorio":
            acerto_aleatorio = [linha_escolhida, coluna_escolhida]
            modo_atual = "busca"
            proximo_ataque = [
                [linha_escolhida + 1, coluna_escolhida],
                [linha_escolhida - 1, coluna_escolhida],
                [linha_escolhida, coluna_escolhida + 1],
                [linha_escolhida, coluna_escolhida - 1]
            ]
            proximo_ataque = filtrar_coordenadas_validas(proximo_ataque, proporcao)

        elif modo_atual == "busca":
            acerto_busca = [linha_escolhida, coluna_escolhida]
            if not verificar_navio_abatido(coords_navios, tabuleiro_atacado):
                modo_atual = "caça"
                proximo_ataque = calcular_proximos_ataques(acerto_aleatorio, acerto_busca, proporcao)
                proximo_ataque = [c for c in proximo_ataque if (c[0], c[1]) not in coordenadas_atacadas]
            else:
                modo_atual = modos_ataque[0]

        elif modo_atual == "caça":
            if verificar_navio_abatido(coords_navios, tabuleiro_atacado):
                modo_atual = "aleatorio"
                acerto_aleatorio = None
                acerto_busca = None
            else:
                proximo_ataque.pop(0)

    elif celula == "~":
        tabuleiro_ataque[linha_escolhida][coluna_escolhida] = "O"
        tabuleiro_atacado[linha_escolhida][coluna_escolhida] = "O"
        placar_ia["IA"]["tiros"] += 1

        if modo_atual == "busca":
            proximo_ataque.pop(0)

        elif modo_atual == "caça":
            if acerto_aleatorio and acerto_busca:
                proximo_ataque = calcular_proximos_ataques(acerto_busca, acerto_aleatorio, proporcao)
                proximo_ataque = [c for c in proximo_ataque if (c[0], c[1]) not in coordenadas_atacadas]
                if not proximo_ataque or proximo_ataque == [[]]:
                    modo_atual = "aleatorio"
                else:
                    modo_atual = "caça"

    jogada_ia.acerto_aleatorio = acerto_aleatorio
    jogada_ia.acerto_busca = acerto_busca
    jogada_ia.modo_atual = modo_atual
    jogada_ia.proximo_ataque = proximo_ataque

def verificar_fim_de_jogo_ia(tabuleiro_atacado):
    if not any("N" in linha for linha in tabuleiro_atacado):
        #time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"A IA acabou com você!")
        print(f"Vitoria da IA!!!")
        return True
    return False

def jogada_ia(tabuleiro_ataque, tabuleiro_atacado, coordenadas_atacadas, proporcao, coords_navios, placar_ia, color):
    parar_evento = threading.Event()
    thread_loading = threading.Thread(target=tela_carregando, args=(parar_evento, "esperando a IA fazer seu ataque"))
    thread_loading.start()

    acerto_aleatorio = getattr(jogada_ia, 'acerto_aleatorio', None)
    acerto_busca = getattr(jogada_ia, 'acerto_busca', None)
    modo_atual = getattr(jogada_ia, 'modo_atual', 'aleatorio')
    proximo_ataque = getattr(jogada_ia, 'proximo_ataque', [[]])

    modos_ataque = ["aleatorio", "busca", "caça"]

    coord_ataque = escolher_coords_ataque_ia(modo_atual, proporcao, proximo_ataque, coordenadas_atacadas)
    linha_escolhida = coord_ataque[0]
    coluna_escolhida = coord_ataque[1]

    aplicar_tiro_ia(modo_atual, proximo_ataque, modos_ataque, coordenadas_atacadas, coords_navios, acerto_aleatorio, proporcao, acerto_busca, tabuleiro_atacado, linha_escolhida, coluna_escolhida, tabuleiro_ataque, placar_ia)

    if verificar_navio_abatido(coords_navios, tabuleiro_atacado):
        placar_ia["IA"]["navios_abatidos"] += 1

    #time.sleep(1.5)
    parar_evento.set()
    thread_loading.join()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"           seu tabuleiro após o ataque")
    printar_tabuleiro(tabuleiro_atacado, color)
    print(f"A IA fez sua jogada!")
    #time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    fim = verificar_fim_de_jogo_ia(tabuleiro_atacado)
    return fim

def tela_carregando(parar_evento, frase):
    pontos = [".", "..", "..."]
    while not parar_evento.is_set():
        for i in pontos:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{frase}{i}")
            #time.sleep(0.25)

def printar_posicionamento_navios(tabuleiro, jogador, color):
    print()
    printar_tabuleiro(tabuleiro, color)
    print()
    print(f"\t Seu posicionamento final! 👆👆")
    #time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Configurações dos navios de {jogador} foram salvas!")
    #time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def definir_proporcao_tabuleiro(color, letras_base, letras):
    proporcao = 0
    while proporcao == 0:
        try:
            proporcao_temp = int(input("Insira o numero que voce quer usar de prorporção para o tabuleiro: "))
            if proporcao_temp < 5:
                print(f"{color['red']}Proporção deve ser no mínimo 5,{color['reset']} tente novamente!")
            if proporcao_temp >= 5:
                proporcao = proporcao_temp
        except Exception:
            print(f"{color['red']}A proporção deve ser numérica,{color['reset']} tente novamente!")

    if proporcao > 26:
        letras_temp = []
        for i in letras_base:
            for j in letras:
                letras_temp.append(f"{i}{j}")
        letras.extend(letras_temp)

    return proporcao

def escolher_modo_jogo(color):
    modo_jogo = input(
        f"Insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

    while modo_jogo != "1" and modo_jogo != "2":
        print(
            f"{color['red']}Erro, tente novamente!{color['reset']} Dessa vez tente usar, apenas 1 ou 2 para seguir com as escolhas.")
        modo_jogo = input(
            f"insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

    return modo_jogo

def inserir_nome_jogadores(modo_jogo, username_um, username_dois):
    if modo_jogo == "1":
        while username_um == "" or username_dois == "":
            username_um = input("Jogador 1, insira seu nome: ")
            username_dois = input("Jogador 2, insira seu nome: ")
            if username_um == "" or username_dois == "":
                print("Erro: Você deve inserir um username para cada jogador!")
                continue


    elif modo_jogo == "2":
        while username_um == "":
            username_um = input("Insira seu username: ")
            if username_um == "":
                print("Erro: Você deve inserir um username!")
                continue

    return username_um, username_dois


def main():
    init()
    color = {
        'blue': Fore.BLUE,
        'green': Fore.GREEN,
        'red': Fore.RED,
        'yellow': Fore.YELLOW,
        'reset': Fore.RESET
    }

    letras = [" "] + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letras_base = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    continuar = ""
    username_um = ""
    username_dois = ""

    modo_jogo = escolher_modo_jogo(color)

    nomes_jogadores = inserir_nome_jogadores(modo_jogo, username_um, username_dois)

    jogador_um = nomes_jogadores[0]
    jogador_dois = nomes_jogadores[1]

    proporcao = definir_proporcao_tabuleiro(color, letras_base, letras)

    while continuar != "X":
        fim = False
        coordenadas_atacadas = set()

        navios = [
            ["Porta-aviões", 5], ["Encouraçado", 4], ["CruzadorUm", 3], ["CruzadorDois", 3], ["SubmarinoUm", 2], ["SubmarinoDois", 2]
        ]

        coords_navios_um = {
            "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],
            "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
        }

        coords_navios_dois = {
            "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],
            "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
        }

        placar = {"jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0},
                  "jogadorDois": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}}

        placar_ia = {"jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0},
                     "IA": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}}

        tabuleiro_um = criar_tabuleiro(proporcao, letras)
        tabuleiro_dois = criar_tabuleiro(proporcao, letras)
        tabuleiro_ataque_um = criar_tabuleiro(proporcao, letras)
        tabuleiro_ataque_dois = criar_tabuleiro(proporcao, letras)
        introducao_jogo(color)

        for i in range(len(coords_navios_um)):
            posicionar_navios(jogador_um, tabuleiro_um, navios[i][1], navios[i][0], proporcao, coords_navios_um, letras, color)

        printar_posicionamento_navios(tabuleiro_um, jogador_um, color)

        if username_dois == "IA":
            for i in range(len(coords_navios_dois)):
                inserir_navios_ia(tabuleiro_dois, navios[i][1], proporcao, navios[i][0], coords_navios_dois)
        else:
            introducao_jogo(color)
            for i in range(len(coords_navios_dois)):
                posicionar_navios(jogador_dois, tabuleiro_dois, navios[i][1], navios[i][0], proporcao, coords_navios_dois, letras, color)

            printar_posicionamento_navios(tabuleiro_dois, jogador_dois, color)

        introducao_batalha()

        while not fim:
            if username_dois == "IA":
                fim = jogada(tabuleiro_um, tabuleiro_ataque_um, tabuleiro_dois, jogador_dois, coords_navios_dois, proporcao, modo_jogo, placar_ia, letras, color, placar, jogador_um)
                if not fim:
                    fim = jogada_ia(tabuleiro_ataque_dois, tabuleiro_um, coordenadas_atacadas, proporcao, coords_navios_um, placar_ia, color)
            else:
                fim = jogada(tabuleiro_um, tabuleiro_ataque_um, tabuleiro_dois, jogador_dois, coords_navios_dois, proporcao, modo_jogo, placar_ia, letras, color, placar,jogador_um)
                if not fim:
                    fim = jogada(tabuleiro_dois, tabuleiro_ataque_dois, tabuleiro_um, jogador_um, coords_navios_um, proporcao, modo_jogo, placar_ia, letras, color, placar, jogador_dois)

        print("-" * 20, "Placar final", "-" * 20)
        if modo_jogo == "1":
            print(f"Comandante {jogador_um}:\n\tTiros: {placar['jogadorUm']['tiros']}\n\tAcertos: {placar['jogadorUm']['acertos']}\n\tNavios abatidos: {placar['jogadorUm']['navios_abatidos']}")
            print(f"Comandante {jogador_dois}:\n\tTiros: {placar['jogadorDois']['tiros']}\n\tAcertos: {placar['jogadorDois']['acertos']}\n\tNavios abatidos: {placar['jogadorDois']['navios_abatidos']}")
        else:
            print(f"Comandante {jogador_um}:\n\tTiros: {placar_ia['jogadorUm']['tiros']}\n\tAcertos: {placar_ia['jogadorUm']['acertos']}\n\tNavios abatidos: {placar_ia['jogadorUm']['navios_abatidos']}")
            print(f"IA:\n\tTiros: {placar_ia['IA']['tiros']}\n\tAcertos: {placar_ia['IA']['acertos']}\n\tNavios abatidos: {placar_ia['IA']['navios_abatidos']}")

        continuar = input(f"pressione{color['yellow']} [ENTER] {color['reset']}para jogar mais uma e insira {color['yellow']}[X]{color['reset']} para parar de jogar: ").upper()

main()