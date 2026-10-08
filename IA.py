import chess
import math

# Define o valor de cada tipo de peça do xadrez
def valor_peca(peca):
    valores = {
        chess.PAWN: 1,       
        chess.KNIGHT: 3,     
        chess.BISHOP: 3,     
        chess.ROOK: 5,       
        chess.QUEEN: 9,      
        chess.KING: 100      
    }

    # Retorna o valor correspondente ao tipo da peça
    return valores[peca.piece_type]


# Avalia o estado atual do tabuleiro
def avaliar_tabuleiro(tabuleiro):
    # Começa com uma pontuação neutra
    valor = 0

    # Percorre todas as peças que estão no tabuleiro
    for peca in tabuleiro.piece_map().values():

        # Se a peça for branca, seu valor é somado
        if peca.color == chess.WHITE:
            valor += valor_peca(peca)

        # Se a peça for preta, seu valor é subtraído
        else:
            valor -= valor_peca(peca)

    # Retorna a avaliação final do tabuleiro
    # Valor positivo = vantagem das brancas
    # Valor negativo = vantagem das pretas
    return valor


# Algoritmo Minimax usado para procurar a melhor jogada
def minimax(tabuleiro, profundidade, maximizando):

    # Para a busca quando chega ao limite de profundidade
    # ou quando o jogo termina
    if profundidade == 0 or tabuleiro.is_game_over():
        return avaliar_tabuleiro(tabuleiro)

    # Quando o jogador está tentando maximizar a pontuação
    if maximizando:

        # Começa com o menor valor possível
        melhor_valor = -math.inf

        # Testa todos os movimentos possíveis
        for movimento in tabuleiro.legal_moves:

            # Faz o movimento temporariamente
            tabuleiro.push(movimento)

            # Continua procurando a melhor jogada
            # diminuindo a profundidade
            valor = minimax(
                tabuleiro,
                profundidade - 1,
                False
            )

            # Desfaz o movimento para testar outro
            tabuleiro.pop()

            # Guarda o maior valor encontrado
            melhor_valor = max(melhor_valor, valor)

        # Retorna a melhor avaliação encontrada
        return melhor_valor

    # Quando o jogador está tentando minimizar a pontuação
    else:

        # Começa com o maior valor possível
        melhor_valor = math.inf

        # Testa todos os movimentos possíveis
        for movimento in tabuleiro.legal_moves:

            # Faz o movimento temporariamente
            tabuleiro.push(movimento)

            # Continua a busca
            # Agora o próximo jogador será o maximizador
            valor = minimax(
                tabuleiro,
                profundidade - 1,
                True
            )

            # Desfaz o movimento
            tabuleiro.pop()

            # Guarda o menor valor encontrado
            melhor_valor = min(melhor_valor, valor)

        # Retorna a pior avaliação para o maximizador
        return melhor_valor


# Procura qual é a melhor jogada disponível
def melhor_jogada(tabuleiro, profundidade):

    # Ainda não temos uma jogada escolhida
    melhor_movimento = None

    # Começa com o menor valor possível
    melhor_valor = -math.inf

    # Percorre todos os movimentos legais
    for movimento in tabuleiro.legal_moves:

        # Faz o movimento temporariamente
        tabuleiro.push(movimento)

        # Avalia o resultado desse movimento
        # A profundidade é diminuída porque uma jogada já foi feita
        valor = minimax(
            tabuleiro,
            profundidade - 1,
            False
        )

        # Desfaz o movimento para testar o próximo
        tabuleiro.pop()

        # Se esse movimento for melhor que o anterior,
        # ele passa a ser a melhor jogada encontrada
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_movimento = movimento

    # Retorna a melhor jogada encontrada pela IA
    return melhor_movimento