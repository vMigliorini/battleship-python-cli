![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

# battleship-python-cli

Jogo completo de Batalha Naval no terminal, feito em Python. Suporta dois modos de jogo — **PvP local** e **contra IA** — com tabuleiro de proporção configurável, posicionamento livre de navios, rastreio de navios abatidos por coordenadas, loading animado e placar ao final.

---

## Funcionalidades

- Modo **Jogador vs Jogador** (mesmo teclado) e **Jogador vs IA**
- Tabuleiro com proporção definida pelo jogador (mínimo 5x5, suporta além de Z com coordenadas AA, AB...)
- Posicionamento de navios na **horizontal** ou **vertical** com validação de limites e sobreposição
- IA com posicionamento e ataques aleatórios
- Rastreio de navios afundados por coordenadas salvas em dicionário
- Tela de loading animada com `threading` durante a vez da IA
- Cores no terminal com `colorama` (água, acerto, erro, navio)
- Placar com tiros, acertos e navios abatidos por jogador

## Navios

| Navio | Tamanho |
|---|---|
| Porta-aviões | 5 |
| Encouraçado | 4 |
| Cruzador (x2) | 3 |
| Submarino (x2) | 2 |

## Pré-requisitos

```bash
pip install colorama
```

## Como executar

```bash
git clone https://github.com/vMigliorini/Batalha-naval.git
cd Batalha-naval
python batalhaNavalCompleto.py
```

## Estrutura do projeto

```
└── batalhaNavalCompleto.py   # Jogo completo em arquivo único
```

---

Desenvolvido por [@vMigliorini](https://github.com/vMigliorini)
