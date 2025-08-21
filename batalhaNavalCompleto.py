import time
import random
import re
import os
import threading
from colorama import Fore, init

def verificarNavioAbatido(statusCoordenadasNavios, tabuleiro, jogador, nomeNavio):
    if not statusCoordenadasNavios.get(nomeNavio):          #verifica se o navio que eu procuro existe no dicionário
        return False                                            
    if all(tabuleiro[coord[0]][coord[1]] == "X" for coord in statusCoordenadasNavios[nomeNavio]):   #verifica se todas as coordenadas salvas do navio estão abatidas
       return True      #se sim, retorna True
    return False
            
def criaMesa(n1):
    tabuleiro = [[" " for _ in range(n1 + 1)] for _ in range(n1 + 1)]       #(n + 1) porque tem uma linha e uma coluna usada para colocar as coordenadas do tabuleiro
    for i in range(1, n1 + 1):                  
        tabuleiro[0][i] = letras[i]                 #coloca itens da lista letra [A, B, B...Z, AA...] na linha 0
    for i in range(1, n1 + 1):
        tabuleiro[i][0] = str(i)                    #coloca números na coluna 0

    for i in range(1, n1 + 1):
        for j in range(1, n1 + 1):
            tabuleiro[i][j] = "~"                   #substitui os lugares que não tem coordenada e estão vazios por "~" agua

    return tabuleiro

def printaMatriz(tabuleiro):
    for i in range(len(tabuleiro)):
        print("\t", end=" ")
        for j in range(len(tabuleiro[i])):
            if i != 0 and j != 0:
                if tabuleiro[i][j] == "~":
                    print(f"{color['blue']}{tabuleiro[i][j]:3}{color['reset']}", end=" ")               #colocando as cores no printaMatriz
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
    while colocouNavios is False:
        try:
            print(f"           Tabuleiro do {jogador}")
            printaMatriz(tabuleiro)
            print()
            print("As coordenadas que você colocar serão a", color['yellow'], "ponta esquerda", color['reset'],
                  "do navio. O resto dele será", color['yellow'], "colocado abaixo ou à direita", color['reset'],
                  "dessa coordenada.")
            coordenadaNavio = ""
            match = None                    

            while match is None:
                coordenadaNavio = input(f"insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do {nomeNavio}: ").upper().replace(" ", "")
                match = re.match(r"(\d+)([A-Z]+)", coordenadaNavio)     #retorna True se o coordenadaNavio seguir o padrão (numero)(navio) usando o "+" para aceitar mais de um item por grupo

                if match is None:               #se não combinar e o match se manter None, volta o coordenadaNavio
                    print(color['red'], "Coordenada inválida,", color['reset'], "Tente novamente!")
                    continue
                tempLinha = int(match.group(1))                 #armazena linha e coluna temporario para poder fazer verificações de erro antes de definir a linha e a coluna
                tempColuna = letras.index(match.group(2))
                if tempLinha > proporcao or tempColuna > proporcao:                 #verifica se está dentro do tabuleiro
                    print(color['red'], "Coordenadas fora do alcance do tabuleiro", color['reset'],", tente novamente!")
                    match = None            #se não o match None serve como uma espécio de return se sair da função para executar o while de novo desde o inicio
                else:
                    linha = int(match.group(1))         #se passar todos os teste é confirmada a linha e a coluna
                    coluna = letras.index(match.group(2))

            direcao = ""
            while direcao not in ["H", "V"]:            #verifica se a direção está no esperado
                direcao = input(f"Insira{color['yellow']} V{color['reset']} para colocar o navio na vertical e {color['yellow']}H{color['reset']} para colocar na horizontal: ").upper().strip()

                if direcao not in ["H", "V"]:               #se não estiver print pra avisar
                    print(color['red'], "Direção inválida,", color['reset'], "Tente novamente!")

            if direcao == "H":
                if coluna + tamanhoNavio - 1 > proporcao:           #verifica se o resto do navio cabe na linha ou coluna proposta
                    print(color['red'], "O navio não cabe na horizontal,", color['reset'], "Tente novamente!")
                    continue

                if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanhoNavio)):       #verifica se a posição que o navio quer ocupar realmente está vazia
                    print(color['red'], "Posição já ocupada,", color['reset'], "Tente novamente!")
                    continue

                coords = []                     #declara fora do for para guardar as coordenadas do navio (util para a verificação de navio abatido)
                for i in range(tamanhoNavio):
                    tabuleiro[linha][coluna + i] = "N"      #posiciona o navio
                    coords.append((linha, coluna + i))          #salva as coordenadas do navio
                statusCoordenadasNavios[nomeNavio] = coords         #adiciona as coordenadas no dicionário de listas
                colocouNavios = True                            #sai do while

            elif direcao == "V":
                if linha + tamanhoNavio - 1 > proporcao:                #mesma coisa só que com as coordenadas na vertical
                    print(color['red'], "Navio não cabe na vertical,", color['reset'], "Tente novamente!")
                    continue

                if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanhoNavio)):
                    print(color['red'], "Posição já ocupada,", color['reset'], "Tente novamente!")
                    continue

                coords = []
                for i in range(tamanhoNavio):
                    tabuleiro[linha + i][coluna] = "N"
                    coords.append((linha + i, coluna))
                statusCoordenadasNavios[nomeNavio] = coords
                colocouNavios = True

        except (ValueError, IndexError):                              #se tiver um erro de valor ou index print para avisar e continue para executar o loop de novo
            print(color['red'], "Coordenada inválida,", color['reset'], " Tente novamente.")
            continue

def introducaoJogo():
    print("\n" + "=" * 50)
    print("🛳🌊 BEM-VINDO AO JOGO BATALHA NAVAL 🌊🛳")
    print("=" * 50)
    print()
    time.sleep(1)
    print(f"\t{color['red']}ATENÇÃO{color['reset']}\n\tA letra {color['green']}[N]{color['reset']} representa as partes do navio que não foram atingidas \n\tA letra {color['red']}[X]{color['reset']} representa acertos nos navios\n\tA letra {color['yellow']}[O]{color['reset']} representa acertos na água")
    print()
    time.sleep(4)
    print(f"\tIniciando a configuração dos navios:")
    print()
    time.sleep(1)
    print(color['green'], "Navios", color['reset'], ":\n\t1 porta-aviões ", color['yellow'], "(5 espaços)",
          color['reset'], "\n\t1 Encouraçado ", color['yellow'], " (4 espaços)", color['reset'], "\n\t2 Cruzador ",
          color['yellow'], "    (3 espaços)", color['reset'], "\n\t2 Submarino ", color['yellow'], "  (2 espaços)",
          color['reset'], "")
    print()

def chamaInsereNavios(jogador, tabuleiro, proporcao, linha, coluna, statusCoordenadasNavios):
    print()

    for i in range(6):                              #essa função serve basicamente para trocar o nome e tamanhho do navio
        if i == 0:
            nomeNavio = "Porta-aviões"
            insereNavios(jogador, tabuleiro, 5, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')

        elif i == 1:
            nomeNavio = "Encouraçado"
            insereNavios(jogador, tabuleiro, 4, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')
        elif i == 2:
            nomeNavio = "CruzadorUm"
            insereNavios(jogador, tabuleiro, 3, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')
        elif i == 3:
            nomeNavio = "CruzadorDois"
            insereNavios(jogador, tabuleiro, 3, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')

        elif i == 4:
            nomeNavio = "SubmarinoUm"
            insereNavios(jogador, tabuleiro, 2, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')
        elif i == 5:
            nomeNavio = "SubmarinoDois"
            insereNavios(jogador, tabuleiro, 2, nomeNavio, proporcao, linha, coluna, statusCoordenadasNavios)
            time.sleep(1)
            os.system('cls')

    print()
    printaMatriz(tabuleiro)
    print()
    print(f"\t Seu posicionamento final! 👆👆")
    time.sleep(2)
    os.system('cls')
    print(f"Configurações dos navios de {jogador} foram salvas!")
    time.sleep(2)
    os.system('cls')

def insereNaviosIA(tabuleiro, tamanhoNavio, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios):
    colocouNavios = False
    while colocouNavios is False:                       #essa função basicamente cria linhas e colunas em posições random até alguma encaixar
        linha = random.randint(1, proporcao)                #gera uma linha e uma coluna aleatória
        coluna = random.randint(1, proporcao)
        direcao = random.choice(["V", "H"])                 #escolhe V ou H
        if direcao == "H":
            coords = []                                 #para armazenar as coordenadas do navio
            if coluna + tamanhoNavio - 1 > proporcao:               #se o navio não couber, repete
                continue

            if any(tabuleiro[linha][coluna + i] != "~" for i in range(tamanhoNavio)):   #se já estiver ocupado, repete
                continue

            for i in range(tamanhoNavio):
                tabuleiro[linha][coluna + i] = "N"
                coords.append((linha, coluna + i))          #armazena as coordenadas na lista
            statusCoordenadasNavios[nomeNavio] = coords     #armazena a lista no dicionário
            colocouNavios = True    #sai do loop

        elif direcao == "V":
            coords = []                             #mesma coisa
            if linha + tamanhoNavio - 1 > proporcao:
                continue

            if any(tabuleiro[linha + i][coluna] != "~" for i in range(tamanhoNavio)):
                continue

            for i in range(tamanhoNavio):
                tabuleiro[linha + i][coluna] = "N"
                coords.append((linha + i, coluna))
            statusCoordenadasNavios[nomeNavio] = coords
            colocouNavios = True

def chamaInsereNaviosIA(tabuleiro, proporcao, linha, coluna, statusCoordenadasNavios):
    pararEvento = threading.Event()
    threadLoading = threading.Thread(target=telaJogadorContraIA,
                                     args=(pararEvento, "esperando a IA colocar os seus navios"))
    threadLoading.start()

    for i in range(6):                                          #mesma coisa da função insereNavios só que sem print
        if i == 0:
            nomeNavio = "Porta-aviões"
            insereNaviosIA(tabuleiro, 5, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
        elif i == 1:
            nomeNavio = "Encouraçado"
            insereNaviosIA(tabuleiro, 4, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
        elif i == 2:
            nomeNavio = "CruzadorUm"
            insereNaviosIA(tabuleiro, 3, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
        elif i == 3:
            nomeNavio = "CruzadorDois"
            insereNaviosIA(tabuleiro, 3, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
        elif i == 4:
            nomeNavio = "SubmarinoUm"
            insereNaviosIA(tabuleiro, 2, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
        elif i == 5:
            nomeNavio = "SubmarinoDois"
            insereNaviosIA(tabuleiro, 2, proporcao, linha, coluna, nomeNavio, statusCoordenadasNavios)
    time.sleep(2)
    pararEvento.set()
    threadLoading.join()

    os.system('cls')
    print(f"configurações dos navios da IA foram criadas!")
    time.sleep(2)
    os.system('cls')

def introducaoBatalha():
    print("\n" + "=" * 60)
    print("🚢  TODOS OS NAVIOS FORAM POSICIONADOS  🚢")
    print("=" * 60)
    time.sleep(1.5)                                                                       #print para o inicio de jogo
    print("🌊💣💥    QUE COMECE A BATALHA!    💥💣🌊")
    print("=" * 60)
    time.sleep(1.5)
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

def jogada(tabuleiro, tabuleiroAtaque, tabuleiroAtacado, jogadorAtacado, jogador,statusCoordenadasNavios):
    print(f"           Tabuleiro com seus navios, comandante {jogador}")
    printaMatriz(tabuleiro)
    print(f"           Tabuleiro de ataque")
    printaMatriz(tabuleiroAtaque)
    print()
    print(f"\t{color['red']}ATENÇÃO{color['reset']}\n\tA letra {color['green']}N{color['reset']} representa as partes do navio que não foram atingidas \n\tA letra {color['red']}X{color['reset']} representa acertos nos navios\n\tA letra {color['yellow']}O{color['reset']} representa acertos na água")
    jogadorPlacar = ""
    if modoJogo == "1":
        if tabuleiro == tabuleiroUm:
            jogadorPlacar = "jogadorUm"
        elif tabuleiro == tabuleiroDois:
            jogadorPlacar = "jogadorDois"
    match = None                
    while match is None:

        coordenadaAtaque = input(f"Insira a coordenada {color['yellow']}(numero)(letra){color['reset']} do seu ataque: ").upper().replace(" ", "")
        match = re.match(r"(\d+)([A-Z]+)", coordenadaAtaque)                                                    #tenta combinar as coordenadas do ataque o a forma (linha)(coluna)
        if match is None:
            print(color['reset'], "Coordenada inválida,", color['reset'], " Tente novamente!")
        else:
            tempLinha = int(match.group(1))                                                     #linha e coluna temporárias para verificar antes de confirmar a linha e coluna
            if match.group(2) in letras:                                #se a coluna estiver na lista letras confirma a coluna aletória
                tempColuna = letras.index(match.group(2))
            else:
                print(color['red'], "Coordenadas fora do alcance do tabuleiro,", color['reset'], " Tente novamente!")
                match = None
                continue
            if proporcao < tempLinha or proporcao < tempColuna:                                         #verifica se as coordenadas estão dentro do tabuleiro
                print(color['red'], "Coordenadas fora do alcance do tabuleiro,", color['reset'], " Tente novamente!")
                match = None
            else:
                linha = int(match.group(1))                             #após os testes, confirma a linha e a coluna
                coluna = letras.index(match.group(2))

    if tabuleiroAtacado[linha][coluna] == "~":              #se estiver vazio, troca no tabuleiro de ataque e no tabuleiro do adversário os itens por "O"
        tabuleiroAtaque[linha][coluna] = "O"
        tabuleiroAtacado[linha][coluna] = "O"
        if modoJogo == "1":
            placar[jogadorPlacar]["tiros"] += 1                 #se estiver jogador x jogador pega o jogadorPlacar(declarado no inicio da def) e adiciona um tiro a mais pra ele
        elif modoJogo == "2":
            placarIA["jogadorUm"]["tiros"] += 1                 #se estiver no modo IA x jogador o jogadorPlacar sempre será jogadorUm então não precisa da variavel jogadorPlacar
    elif tabuleiroAtacado[linha][coluna] == "N":                #se for navio, vira "X"
        tabuleiroAtaque[linha][coluna] = "X"
        tabuleiroAtacado[linha][coluna] = "X"
        if modoJogo == "2":
            placarIA["jogadorUm"]["acertos"] += 1           #aumenta os acertos e tiros
            placarIA["jogadorUm"]["tiros"] += 1             
        elif modoJogo == "1":
            placar[jogadorPlacar]["tiros"] += 1
            placar[jogadorPlacar]["acertos"] += 1
    else:
        print(f"{color['red']}Voce atirou duas vezes no mesmo lugar,{color['reset']}Cuidado!")
        time.sleep(2)

    naviosInimigos = ["Porta-aviões", "Encouraçado", "CruzadorUm", "CruzadorDois", "SubmarinoUm", "SubmarinoDois"]      #pega o nome dos navios
    naviosAfundadosContador = 0                                                                                         #inicializa um contador de navios afundados
    if modoJogo == "1":                                                                                                          #jogador x jogador:
        for nomeDoNavio in naviosInimigos:                                                                      #chama verificarNavioAbatido e se retornar True aumenta o contador 
            if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado, jogador, nomeDoNavio):
                naviosAfundadosContador += 1
        placar[jogadorPlacar]["navios_abatidos"] = naviosAfundadosContador                                      #coloca o resultado do contador dentro do placar
    if modoJogo == "2":
        for nomeDoNavio in naviosInimigos:
            if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado, jogador, nomeDoNavio):
                naviosAfundadosContador += 1
        placarIA["jogadorUm"]["navios_abatidos"] = naviosAfundadosContador                                              #coloca o resultado do contador dentro do placarIA

    os.system('cls')
    print(f"           Tabuleiro de ataque do comandante {jogador}")
    printaMatriz(tabuleiroAtaque)
    print(f"\tEssa foi sua jogada, {jogador}. Passe a vez para o outro jogador!")
    time.sleep(5)
    os.system('cls')

    if not any("N" in linha for linha in tabuleiroAtacado):             #verifica se ainda tem navio nas linhas, se não declara o fim do jogo e retorna True para a variavel fim que chama a jogada
        time.sleep(2)
        os.system('cls')
        print(f"Voce acabou com o {jogadorAtacado}!")
        print(f"Vitoria de {jogador}!!!")
        return True
    return False                                                        #continua o jogo
        
def jogadaIAComEspera(tabuleiroAtaque, tabuleiroAtacado, coordenadasAtacadas, proporcao, statusCoordenadasNavios, jogador, tabuleiro):
    pararEvento = threading.Event()
    threadLoading = threading.Thread(target=telaJogadorContraIA, args=(pararEvento, "esperando a IA fazer seu ataque"))
    threadLoading.start()

    atacou = False
    while not atacou:
        linhaRandom = random.randint(1, proporcao)                  #gera linhas e colunas random
        colunaRandom = random.randint(1, proporcao)
        if (linhaRandom, colunaRandom) not in coordenadasAtacadas:                      #verifica se a IA já atacou a coordenada
            coordenadasAtacadas.add((linhaRandom, colunaRandom))            #adiciona a coordenada para o conjunto
            if tabuleiroAtacado[linhaRandom][colunaRandom] == "~":                 #substitui o resultado do tiro nos tabuleiro e atualiza os placares
                tabuleiroAtaque[linhaRandom][colunaRandom] = "O"
                tabuleiroAtacado[linhaRandom][colunaRandom] = "O"
                placarIA["IA"]["tiros"] += 1
                atacou = True                                   #fim do loop
            elif tabuleiroAtacado[linhaRandom][colunaRandom] == "N":
                tabuleiroAtaque[linhaRandom][colunaRandom] = "X"
                tabuleiroAtacado[linhaRandom][colunaRandom] = "X"
                placarIA["IA"]["tiros"] += 1
                placarIA["IA"]["acertos"] += 1
                atacou = True                                               #fim do loop

    naviosInimigos = ["Porta-aviões", "Encouraçado", "CruzadorUm", "CruzadorDois", "SubmarinoUm", "SubmarinoDois"]      #pega os nomes para chamar a função
    naviosAfundadosContador = 0                                                                                         #inicia o contador
    for nomeDoNavio in naviosInimigos:
        if verificarNavioAbatido(statusCoordenadasNavios, tabuleiroAtacado, jogador, nomeDoNavio):          #chama a função se retornar True aumenta a quantidade de navios abatidos
            naviosAfundadosContador += 1
    placarIA["IA"]["navios_abatidos"] = naviosAfundadosContador             #atualiza o placar


    time.sleep(1.5)
    pararEvento.set()
    threadLoading.join()

    os.system('cls')
    print(f"           seu tabuleiro após o ataque")
    printaMatriz(tabuleiroAtacado)
    print(f"A IA fez sua jogada!")
    time.sleep(1)
    os.system('cls')

    if not any("N" in linha for linha in tabuleiroAtacado):         #se não houver mais navios nas linhas decreta o fim do jogo
        time.sleep(2)
        os.system('cls')
        print(f"A IA acabou com você!")
        print(f"Vitoria da IA!!!")
        return True                                 #fim de jogo
    else:
        return False                                    #continua o jogo

def telaJogadorContraIA(pararEvento, frase):
    pontos = [".", "..", "..."]         #com o import threading a gente pôde deixar uma tela de espera na tela enquanto a IA faz sua jogada, e usanddo essa lista pode ficar atualizando a tela com um lopp dor
    while not pararEvento.is_set():
        for i in pontos:
            os.system('cls')
            print(f"{frase}{i}")                #input da frase, no caso do insereNaviosIa é: "esperando a IA colocar seus navios"
            time.sleep(0.25)

init()       # init para a biblioteca Colorama
color = {                 # dicionarios para as cores
    'blue': Fore.BLUE,
    'green': Fore.GREEN,
    'red': Fore.RED,
    'yellow': Fore.YELLOW,
    'reset': Fore.RESET
}
placar = {       # Dicionaios para o placar, dai so adicionamos os valores
    "jogadorUm": {
        "tiros": 0,
        "acertos": 0,
        "navios_abatidos": 0
    },
    "jogadorDois": {
        "tiros": 0,
        "acertos": 0,
        "navios_abatidos": 0
    }
}
placarIA = {
    "jogadorUm": {
        "tiros": 0,
        "acertos": 0,
        "navios_abatidos": 0
    },
    "IA": {
        "tiros": 0,
        "acertos": 0,
        "navios_abatidos": 0
    }
}
            # lista letras que começa no vazio para a funcionalidade da obtenção da coluna nas funçoes de jogada e inserir navios. Além de servir para colocar as coordenadas no tabuleiro
letras = [" "] + ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
letrasDois = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
linha = 0             
coluna = 0
proporcao = 0
continuar = ""
jogadorUm = []    
jogadorDois = []
portaAvioes = 5     # tamanhos dos navios
encouracado = 4
cruzador = 3
submarino = 2

 
modoJogo = input(f"Insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

while modoJogo != "1" and modoJogo != "2":      #se o input for inválido o código pede o input de novo, até obter um resultado satisfatório
    print(color['red'], "Erro, tente novamente!", color['reset']," Dessa vez tente usar, apenas 1 ou 2 para seguir com as escolhas.")
    modoJogo = input(f"insira {color['yellow']}[1]{color['reset']} se voce quer jogar contra um adversário local ou digite {color['yellow']}[2]{color['reset']} se voce quer jogar contra IA: ")

if modoJogo == "1":  # condicao para utilizacao das variaveis coretas de acordo com o modo de jogo 
    usernameUm = input("Jogador 1, insira seu nome: ")        
    usernameDois = input("Jogador 2, insira seu nome: ") 
    jogadorUm.append(usernameUm)                              # adicao na listas dos jogadores 
    jogadorDois.append(usernameDois)
 
elif modoJogo == "2":    # condicao para utilizacao das variaveis coretas de acordo com o modo de jogo 
    usernameUm = input("Insira seu username: ")
    usernameDois = "IA"
    jogadorUm.append(usernameUm)
    jogadorDois.append(usernameDois)

proporcao = 0
while proporcao == 0:     # continua até a proporção receber um valor
    try:
        proporcaoTemp = int(input("Insira o numero que voce quer usar de prorporção para o tabuleiro: "))
        if proporcaoTemp < 5:                # condicao de minimo do tabuleiro jogável
            print(f"{color['red']}Proporção deve ser no mínimo 5,{color['reset']} tente novamente!")
        if proporcaoTemp >= 5:               
            proporcao = proporcaoTemp
    except (ValueError, IndexError):        
        print(color['red'], "A proporção deve ser numérica,", color['reset'], " tente novamente!")

if proporcao > 26:    # se a proporção for maior que 26 a lista letras vai receber cordenadas AA, AB, AC...BA, BB...ZZ.
    letrasTemp = []

    for i in letrasDois:
        for j in letras:
            letrasTemp.append(f"{i}{j}")        #usado para gerar esse padrão AA, AB...
    letras.extend(letrasTemp)           #adiciona essa lista criada para o letras

while continuar != "X": # Esse while coloca a condicao de o jogador continuar (jogar mais uma vez) ou terminar o jogo, X contina e enter termina
    fim = False         
    coordenadasAtacadas = set() 
    statusCoordenadasNaviosUm = {                                 # Criacao de um dicionario para contar os Navios_abatidos a cada novo jogo
        "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],  
        "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
    }
    statusCoordenadasNaviosDois = {
        "Porta-aviões": [], "Encouraçado": [], "CruzadorUm": [],  
        "CruzadorDois": [], "SubmarinoUm": [], "SubmarinoDois": []
    }
    placar = { "jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}, "jogadorDois": {"tiros": 0, "acertos": 0, "navios_abatidos": 0} } # reiniciando o placar
    placarIA = { "jogadorUm": {"tiros": 0, "acertos": 0, "navios_abatidos": 0}, "IA": {"tiros": 0, "acertos": 0, "navios_abatidos": 0} }
    tabuleiro = criaMesa(proporcao)
    tabuleiroUm = criaMesa(proporcao)
    tabuleiroDois = criaMesa(proporcao)
    tabuleiroAtaqueUm = criaMesa(proporcao)
    tabuleiroAtaqueDois = criaMesa(proporcao)       #recriando os tabuleiros
    introducaoJogo()
    chamaInsereNavios(jogadorUm, tabuleiroUm, proporcao, linha, coluna, statusCoordenadasNaviosUm)
    
    if usernameDois == "IA": 
        chamaInsereNaviosIA(tabuleiroDois, proporcao, linha, coluna, statusCoordenadasNaviosDois)       #caso o jogador estiver contra IA chama a função chamaInsereNaviosIA
    else:                     
        introducaoJogo()                                                                               #em outro caso, chama a função chamaInsereNavios
        chamaInsereNavios(jogadorDois, tabuleiroDois, proporcao, linha, coluna, statusCoordenadasNaviosDois)

    introducaoBatalha()      

    while fim is False:  # Esse laco continua ate que alguem ganhe, ele que mantem o jogo acontecendo
        if usernameDois == "IA": # verifica se voce esta contra IA
            fim = jogada(tabuleiroUm, tabuleiroAtaqueUm, tabuleiroDois, jogadorDois, jogadorUm, statusCoordenadasNaviosDois) # Essa condicao é muito importante, para fazer o jogo parar
            if fim is False:                                                                                                 # entao dependendo do que a def jogada retornar o jogo acaba, no caso se retornar True o jogo acaba
                fim = jogadaIAComEspera(tabuleiroAtaqueDois, tabuleiroUm, coordenadasAtacadas, proporcao, statusCoordenadasNaviosUm,jogadorDois, tabuleiroDois) 

        else: # caso nao seja contra IA ele puxa a jogada certa para continuar 
            fim = jogada(tabuleiroUm, tabuleiroAtaqueUm, tabuleiroDois, jogadorDois, jogadorUm, statusCoordenadasNaviosDois)# mesma condicao do de cima porem, sem a IA 
            if fim is False: 
                fim = jogada(tabuleiroDois, tabuleiroAtaqueDois, tabuleiroUm, jogadorUm, jogadorDois, statusCoordenadasNaviosUm)

    print("-" * 20, "Placar final", "-" * 20) 
    if modoJogo == "1": # condicao printar o placar certo, ja colorido, separando os modos 
        print(f"Comandante {jogadorUm}:\n\tTiros: {placar['jogadorUm']['tiros']}\n\tAcertos: {placar['jogadorUm']['acertos']}\n\tNavios abatidos: {placar['jogadorUm']['navios_abatidos']}") # prints do placar 
        print(f"Comandante {jogadorDois}:\n\tTiros: {placar['jogadorDois']['tiros']}\n\tAcertos: {placar['jogadorDois']['acertos']}\n\tNavios abatidos: {placar['jogadorDois']['navios_abatidos']}")
    else: #else para printar o placar correto 
        print(f"Comandante {jogadorUm}:\n\tTiros: {placarIA['jogadorUm']['tiros']}\n\tAcertos: {placarIA['jogadorUm']['acertos']}\n\tNavios abatidos: {placarIA['jogadorUm']['navios_abatidos']}")
        print(f"IA:\n\tTiros: {placarIA['IA']['tiros']}\n\tAcertos: {placarIA['IA']['acertos']}\n\tNavios abatidos: {placarIA['IA']['navios_abatidos']}")

    continuar = input(f"pressione{color['yellow']} [ENTER] {color['reset']}para jogar mais uma e insira {color['yellow']}[X]{color['reset']} para parar de jogar: ").upper()