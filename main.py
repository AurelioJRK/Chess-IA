import chess
import IA
import dados
import tabuleiro  as tb
import time

pecas_promo = { # Mapeamento das peças de promoção
    "r": "t",
    "n": "c",
    "b": "b",
    "q": "r",
}

def jogada_humana(posicao): # Solicita ao jogador humano que insira uma jogada e valida se é legal
    movimento = input(f"Digite sua jogada (ex: e2e4): ").strip().lower()

    try:
        if len(movimento) not in (4, 5):
            print("Movimento inválido. Certifique-se de digitar no formato correto (ex: e2e4).")
            return None

        origem = chess.parse_square(movimento[:2])
        destino = chess.parse_square(movimento[2:4])
        peca = posicao.piece_at(origem)

        if (peca is None) or (peca.piece_type == chess.PAWN and chess.square_rank(destino) in [0, 7]):

            promocao_legal = [ #verifica se a promoção é legal
                jogada for jogada in posicao.legal_moves
                if jogada.from_square == origem and jogada.to_square == destino and jogada.promotion is not None
            ]
            if not promocao_legal:
                print("Movimento inválido. Promoção não permitida para essa jogada.")
                return None

            if len(movimento) == 4:
                promocao = input("promover para torre, cavalo, bispo ou rainha? (t, c, b, r): ").strip().lower()

                if promocao not in pecas_promo:
                    print("Peça de promoção inválida.")
                    return None

                movimento += pecas_promo[promocao]

            else:
                promocao = movimento[4]

                if promocao not in pecas_promo:
                    print("Peça de promoção inválida.")
                    return None

            movimento = movimento[:4] + pecas_promo[promocao]
        jogada = chess.Move.from_uci(movimento)

        if jogada not in posicao.legal_moves:
            print("Movimento inválido.")
            return None

        return jogada

    except ValueError:
        print("formato inválido. Certifique-se de digitar no formato correto (ex: e2e4).")
        return None

def jogar(modo): # Função principal para jogar uma partida de xadrez, seja contra a IA ou entre duas IAs

    tempo_espera = 1  # Tempo de espera entre os movimentos da IA (em segundos)

    if modo == "IA vs IA":
        while True:
            try:
                tempo_espera = float(input("Digite o tempo de espera entre os movimentos da IA (ex: 1.5): "))

                if tempo_espera >= 0:
                    break

                print("O tempo de espera deve ser um número não negativo. Tente novamente.")

            except ValueError:
                print("Entrada inválida. Certifique-se de digitar um número válido (ex: 1.5).")


    posicao = chess.Board()

    if modo == "humano vs IA":
        brancas = "humano"
        pretas = "IA"
        versao_brancas = "Humano"
        versao_pretas = IA.versao_IA

    else:
        brancas = "IA"
        pretas = "IA"
        versao_brancas = IA.versao_IA
        versao_pretas = IA.versao_IA2

    partida_id = dados.iniciar_partida(
        modo=modo,
        brancas=brancas,
        pretas=pretas,
        versao_brancas=versao_brancas,
        versao_pretas=versao_pretas
    )

    total_jogadas = 0
    limite_jogadas = 200  # Limite de jogadas para evitar partidas muito longas
    interrompida= False

    while not posicao.is_game_over(claim_draw = True):

        if total_jogadas >= limite_jogadas:
            print("Limite de jogadas atingido. A partida será encerrada.")
            interrompida = True
            break

        tb.mostrar_tabuleiro(posicao)

        if posicao.turn == chess.WHITE:  # Vez das brancas
            jogador = brancas
            versao = versao_brancas
            cor = "brancas"
        else:  # Vez das pretas
            jogador = pretas
            versao = versao_pretas
            cor = "pretas"

        print(f"\n Vez das {cor}: {jogador}")

        if jogador == "humano":
            jogada = jogada_humana(posicao)

            if jogada is None:
                print("Movimento inválido. Tente novamente.")
                continue

        else:
            jogada = IA.melhor_jogada(posicao, IA.profundidade_IA)

            if jogada is None or jogada not in posicao.legal_moves:
                print("A IA não conseguiu encontrar uma jogada válida. A partida será encerrada.")
                interrompida = True
                break

            print(f"IA jogou: {posicao.uci(jogada)}")

        posicao.push(jogada)
        total_jogadas += 1
        if modo == "IA vs IA":
            time.sleep(tempo_espera)

    tb.mostrar_tabuleiro(posicao)
    print("\nPartida encerrada.")

    if not interrompida:
        resultado = posicao.result(claim_draw=True)
        if resultado == "1-0":
            print("Brancas venceram!")
            motivo = "checkmate" if posicao.is_checkmate() else "resignation"
        elif resultado == "0-1":
            print("Pretas venceram!")
            motivo = "checkmate" if posicao.is_checkmate() else "resignation"
        else:
            print("Empate!")
            motivo = "draw"

        dados.finalizar_partida(partida_id, posicao)

        print(f"\n desempenho das IAs:")
        print(dados.resumo_desempenho().to_string(index=False))
    else:
        print("A partida foi interrompida antes de ser concluída. Nenhum resultado será registrado.")

    input("\n Pressione Enter para voltar ao menu principal...")

def menu(): # Exibe o menu principal do jogo e permite ao usuário escolher entre jogar contra a IA, assistir a uma partida entre IAs ou sair do jogo
    while True:
        print("\n=== Jogo de Xadrez com IA ===")
        print("1. Humano vs IA")
        print("2. IA vs IA")
        print("3. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            jogar("humano vs IA")
        elif escolha == "2":
            jogar("IA vs IA")
        elif escolha == "3":
            print("Saindo do jogo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()