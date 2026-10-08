import chess
import IA

tabuleiro = chess.Board()

simbolos = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚"
}

while not tabuleiro.is_game_over():

    print("\n")
    print("     a     b     c     d     e     f     g     h")
    print("   +" + "-----+" * 8)

    for linha in range(8, 0, -1):

        print(f" {linha} |", end="")

        for coluna in range(8):

            casa = chess.square(coluna, linha - 1)
            peca = tabuleiro.piece_at(casa)

            if peca:
                simbolo = simbolos[peca.symbol()]
            else:
                simbolo = " "

            print(f"  {simbolo}  |", end="")

        print(f" {linha}")
        print("   +" + "-----+" * 8)

    print("     a     b     c     d     e     f     g     h")

    if tabuleiro.turn == chess.WHITE:

        movimento = input("Sua jogada: ")

        jogada = chess.Move.from_uci(movimento)

        if jogada in tabuleiro.legal_moves:
            tabuleiro.push(jogada)
        else:
            print("Movimento ilegal!")

    else:

        print("Vez da IA (Pretas)")

        jogada = IA.melhor_jogada(tabuleiro, 2)

        tabuleiro.push(jogada)

        print("IA jogou:", jogada)

print("\nJogo terminado!")

if tabuleiro.is_checkmate():
    vencedor = "Brancas" if not tabuleiro.turn else "Pretas"
    print("Xeque-mate!")
    print("Vencedor:", vencedor)
else:
    print("Empate!")