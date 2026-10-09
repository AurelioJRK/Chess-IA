import chess
import IA
import dados

versao_ia = "IA_v1"

simbolos = {
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
                if len(movimento) != 4:
                    origem = chess.parse_square(movimento[:2])
                    destino = chess.parse_square(movimento[2:4])

                    peca = tabuleiro.piece_at(origem)

                    if peca and peca.piece_type == chess.PAWN and (
                        (peca.color == chess.WHITE and destino >= chess.A8) or
                        (peca.color == chess.BLACK and destino <= chess.H1)
                    ):
                        promocao = input(
                            "Escolha a peça para promoção (R, T, B, C): "
                        ).strip().lower()

                        if promocao == "r":
                            movimento = chess.Move(origem, destino, promotion=chess.QUEEN)
                        elif promocao == "t":
                            movimento = chess.Move(origem, destino, promotion=chess.ROOK)
                        elif promocao == "b":
                            movimento = chess.Move(origem, destino, promotion=chess.BISHOP)
                        elif promocao == "c":
                            movimento = chess.Move(origem, destino, promotion=chess.KNIGHT)
                        else:
                            print("Peça inválida para promoção!")
                            continue

                        movimento += promocao
                        
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

            print("Seu rei está em xeque:", tabuleiro.is_check())
            print("A IA consegue dar xeque-mate em uma jogada?")

            for movimento in tabuleiro.legal_moves:
                tabuleiro.push(movimento)

                if tabuleiro.is_checkmate():
                    print("Mate encontrado:", movimento)

        tabuleiro.pop()

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