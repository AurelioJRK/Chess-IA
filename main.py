import chess
import IA
import dados

versao_ia = "IA_v1"

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


while True:
    tabuleiro = chess.Board()

    partida_id = dados.iniciar_partida(
        modo="humano_vs_ia",
        brancas="humano",
        pretas="IA",
        versao_brancas="humano",
        versao_pretas=versao_ia
    )

    while not tabuleiro.is_game_over(claim_draw=True):

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
            movimento = input("Sua jogada (ex.: e2e4): ").strip()

            try:
                jogada = chess.Move.from_uci(movimento)

                if jogada in tabuleiro.legal_moves:
                    dados.registrar_movimento(
                        partida_id,
                        tabuleiro,
                        jogada,
                        jogador="humano"
                    )

                    tabuleiro.push(jogada)

                else:
                    print("Movimento ilegal!")

            except ValueError:
                print("Formato inválido! Digite no formato e2e4.")

        else:
            print("Vez da IA (Pretas)")

            jogada = IA.melhor_jogada(tabuleiro, 3)  # A profundidade de busca pode ser ajustada conforme necessário

            if jogada is None:
                break

            print("IA jogou:", tabuleiro.uci(jogada))

            dados.registrar_movimento(
                partida_id,
                tabuleiro,
                jogada,
                jogador="IA",
                versao_ia=versao_ia
            )

            tabuleiro.push(jogada)

    print("\nJogo terminado!")

    if tabuleiro.is_checkmate():
        vencedor = "Brancas" if tabuleiro.turn == chess.BLACK else "Pretas"
        print("Xeque-mate!")
        print("Vencedor:", vencedor)
    else:
        print("Empate!")

    dados.finalizar_partida(partida_id, tabuleiro)

    print("\nDesempenho da IA:")
    print(dados.resumo_desempenho().to_string(index=False))

    escolha = input(
        "\nDeseja jogar novamente? (s/n): "
    ).strip().lower()

    if escolha != "s":
        print("Obrigado por jogar!")
        break