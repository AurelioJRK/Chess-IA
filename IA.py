import chess
import math

versao_IA = "MM1v2"  # Versão da IA que você deseja usar (por enquanto muda somente o nome no banco de dados)
versao_IA2 = "MM2v2"  # Versão da IA que você deseja usar (por enquanto muda somente o nome no banco de dados)
profundidade_IA = 2  # Profundidade de busca da IA (Quantidade de movimentos à frente que a IA irá considerar,
#quanto maior o numero mais pesado sera o processamento

def valor_peca(peca): # Retorna o valor da peça com base no seu tipo
    valores = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
 

    return valores[peca.piece_type]

VALOR_PENALIDADE_REPETICAO = 0.3
valor_mate = 10000  # Valor para checkmate

def avaliar_tabuleiro(tabuleiro): # Avalia o tabuleiro e retorna um valor numérico representando a vantagem de um jogador sobre o outro
    if tabuleiro.is_checkmate():
        if tabuleiro.turn == chess.WHITE:
            return -valor_mate
        return valor_mate

    if tabuleiro.is_game_over():
        return 0

    valor = 0

    for casa, peca in tabuleiro.piece_map().items():
        pontos = valor_peca(peca)

        coluna = chess.square_file(casa)
        linha = chess.square_rank(casa)

        centro = 3.5 - (
            abs(coluna - 3.5) + abs(linha - 3.5)
        ) / 2

        if peca.piece_type == chess.PAWN:
            pontos += max(0, centro) * 0.12

            if peca.color == chess.WHITE:
                pontos += linha * 0.08
            else:
                pontos += (7 - linha) * 0.08

        elif peca.piece_type == chess.KNIGHT:
            pontos += centro * 0.25

        elif peca.piece_type == chess.BISHOP:
            pontos += centro * 0.12

        elif peca.piece_type == chess.QUEEN:
            pontos += centro * 0.04

        if peca.piece_type in (chess.KNIGHT, chess.BISHOP):
            if peca.color == chess.WHITE:
                casas_iniciais = (
                    [chess.B1, chess.G1]
                    if peca.piece_type == chess.KNIGHT
                    else [chess.C1, chess.F1]
                )
            else:
                casas_iniciais = (
                    [chess.B8, chess.G8]
                    if peca.piece_type == chess.KNIGHT
                    else [chess.C8, chess.F8]
                )

            if casa not in casas_iniciais:
                pontos += 0.25

        if peca.piece_type == chess.KING:
            casas_roque = (
                [chess.G1, chess.C1]
                if peca.color == chess.WHITE
                else [chess.G8, chess.C8]
            )

            if casa in casas_roque:
                pontos += 1.5

        if peca.color == chess.WHITE:
            valor += pontos
        else:
            valor -= pontos

    return valor

def penalidade_repeticao(tabuleiro, movimento): # Aplica uma penalidade para movimentos repetidos, desestimulando a IA a repetir jogadas
    if len(tabuleiro.move_stack) < 2:
        return 0

    movimento_anterior = tabuleiro.move_stack[-2]

    if (
        movimento.from_square == movimento_anterior.to_square
        and movimento.to_square == movimento_anterior.from_square
    ):
        return (
            -VALOR_PENALIDADE_REPETICAO
            if tabuleiro.turn == chess.WHITE
            else VALOR_PENALIDADE_REPETICAO
        )

    return 0

def minimax(tabuleiro, profundidade, maximizando): # Implementa o algoritmo Minimax para encontrar a melhor jogada possível para a IA
    if profundidade == 0 or tabuleiro.is_game_over():
        return avaliar_tabuleiro(tabuleiro)

    if maximizando:
        melhor_valor = -math.inf

        for movimento in tabuleiro.legal_moves:
            penalidade = penalidade_repeticao(tabuleiro, movimento)
            tabuleiro.push(movimento)

            valor = minimax(
                tabuleiro,
                profundidade - 1,
                False
            )

            tabuleiro.pop()

            valor += penalidade
            melhor_valor = max(melhor_valor, valor)

        return melhor_valor

    else:
        melhor_valor = math.inf

        for movimento in tabuleiro.legal_moves:
            penalidade = penalidade_repeticao(tabuleiro, movimento)
            tabuleiro.push(movimento)

            valor = minimax(
                tabuleiro,
                profundidade - 1,
                True
            )

            tabuleiro.pop()

            valor += penalidade
            melhor_valor = min(melhor_valor, valor)

        return melhor_valor

def melhor_jogada(tabuleiro, profundidade): # Encontra a melhor jogada possível para a IA usando o algoritmo Minimax

    melhor_movimento = None

    maximizando = tabuleiro.turn == chess.WHITE

    melhor_valor = (
        -math.inf if maximizando else math.inf
    )

    for movimento in tabuleiro.legal_moves:
        penalidade = penalidade_repeticao(
            tabuleiro,
            movimento
        )

        tabuleiro.push(movimento)

        valor = minimax(
            tabuleiro,
            profundidade - 1,
            not maximizando
        )

        tabuleiro.pop()

        valor += penalidade

        if maximizando and valor > melhor_valor:
            melhor_valor = valor
            melhor_movimento = movimento

        elif not maximizando and valor < melhor_valor:
            melhor_valor = valor
            melhor_movimento = movimento

    return melhor_movimento
