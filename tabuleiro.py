import chess
import main

SIMBOLOS = {
    "p": "♙",
    "n": "♘",
    "b": "♗",
    "r": "♖",
    "q": "♕",
    "k": "♔",
    "P": "♟",
    "N": "♞",
    "B": "♝",
    "R": "♜",
    "Q": "♛",
    "K": "♚"
}


def mostrar_tabuleiro(tabuleiro):
    print("\n")
    print("     a     b     c     d     e     f     g     h")
    print("   +" + "-----+" * 8)

    for linha in range(8, 0, -1):
        print(f" {linha} |", end="")

        for coluna in range(8):
            casa = chess.square(coluna, linha - 1)
            peca = tabuleiro.piece_at(casa)

            if peca:
                simbolo = SIMBOLOS[peca.symbol()]
            else:
                simbolo = " "

            print(f"  {simbolo}  |", end="")

        print(f" {linha}")
        print("   +" + "-----+" * 8)
