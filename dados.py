import csv
import os
import pandas as pd

pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
arquivo_partidas = os.path.join(pasta, "partidas.csv")
arquivo_movimentos = os.path.join(pasta, "movimentos.csv")
arquivo_desempenho = os.path.join(pasta, "desempenho.csv")

colunas_partidas = [
    "partida_id",
    "modo",
    "brancas",
    "pretas",
    "versao_brancas",
    "versao_pretas",
    "resultado",
    "motivo",
    "total_jogadas"
]

colunas_movimentos = [
    "partida_id",
    "numero_jogada",
    "jogador",
    "cor",
    "versao_ia",
    "movimento_uci",
    "movimento_san",
    "fen_antes",
    "fen_depois"
]

colunas_desempenho = [
    "partida_id",
    "versao_ia",
    "resultado",
    "pontos"
]

def criar_arquivo(caminho, colunas): # Cria o arquivo CSV se ele não existir

    os.makedirs(pasta, exist_ok=True)

    if not os.path.exists(caminho):
        pd.DataFrame(columns=colunas).to_csv(
            caminho,
            index=False,
            encoding="utf-8"
        )

def gerar_id_partida(): # Gera um novo ID de partida com base no último ID registrado no arquivo CSV de partidas
    criar_arquivo(arquivo_partidas, colunas_partidas)

    partidas = pd.read_csv(
        arquivo_partidas,
        dtype=str
    )

    if partidas.empty:
        return "00001"

    ids = pd.to_numeric(
        partidas["partida_id"],
        errors="coerce"
    ).dropna()

    if ids.empty:
        return "00001"

    proximo_id = int(ids.max()) + 1

    return str(proximo_id).zfill(5)

def iniciar_partida(modo, brancas, pretas, versao_brancas, versao_pretas):  # Inicia uma nova partida e retorna o ID da partida

    criar_arquivo(arquivo_partidas, colunas_partidas)
    criar_arquivo(arquivo_movimentos, colunas_movimentos)
    criar_arquivo(arquivo_desempenho, colunas_desempenho)

    partida_id = gerar_id_partida()

    nova_partida = pd.DataFrame([{
        "partida_id": partida_id,
        "modo": modo,
        "brancas": brancas,
        "pretas": pretas,
        "versao_brancas": versao_brancas,
        "versao_pretas": versao_pretas,
        "resultado": "",
        "motivo": "",
        "total_jogadas": 0
    }])

    nova_partida.to_csv(arquivo_partidas, mode="a", header=False, index=False)

    return partida_id

def registrar_movimento(  # Registra um movimento no arquivo CSV de movimentos
    partida_id,
    tabuleiro,
    jogada,
    jogador,
    versao_ia=""
):
    criar_arquivo(arquivo_movimentos, colunas_movimentos)

    fen_antes = tabuleiro.fen()
    movimento_san = tabuleiro.san(jogada)
    numero_jogada = len(tabuleiro.move_stack) + 1

    cor = "brancas" if tabuleiro.turn else "pretas"

    tabuleiro_futuro = tabuleiro.copy()
    tabuleiro_futuro.push(jogada)

    fen_depois = tabuleiro_futuro.fen()

    novo_movimento = pd.DataFrame([{
        "partida_id": partida_id,
        "numero_jogada": numero_jogada,
        "jogador": jogador,
        "cor": cor,
        "versao_ia": versao_ia,
        "movimento_uci": jogada.uci(),
        "movimento_san": movimento_san,
        "fen_antes": fen_antes,
        "fen_depois": fen_depois
    }])

    novo_movimento.to_csv(
        arquivo_movimentos,
        mode="a",
        header=False,
        index=False,
        encoding="utf-8"
    )

def finalizar_partida(partida_id, tabuleiro):  # Finaliza a partida e registra o resultado no arquivo CSV de partidas e desempenho
    criar_arquivo(arquivo_partidas, colunas_partidas)
    criar_arquivo(arquivo_desempenho, colunas_desempenho)

    if not tabuleiro.is_game_over(claim_draw=True):
        raise ValueError("A partida ainda não terminou.")

    partidas = pd.read_csv(
        ARQUIVO_PARTIDAS,
        dtype=str
    ).fillna("")

    indice = partidas.index[
        partidas["partida_id"] == partida_id
    ]

    if len(indice) == 0:
        raise ValueError("Partida não encontrada.")

    i = indice[0]

    resultado = tabuleiro.result(claim_draw=True)
    desfecho = tabuleiro.outcome(claim_draw=True)

    motivos = {
        "CHECKMATE": "xeque-mate",
        "STALEMATE": "afogamento",
        "INSUFFICIENT_MATERIAL": "material insuficiente",
        "SEVENTYFIVE_MOVES": "regra dos 75 lances",
        "FIVEFOLD_REPETITION": "repetição de posição",
        "FIFTY_MOVES": "regra dos 50 lances",
        "THREEFOLD_REPETITION": "repetição de posição"
    }

    motivo = motivos.get(
        desfecho.termination.name,
        desfecho.termination.name.lower()
    )

    partidas.loc[i, "resultado"] = resultado
    partidas.loc[i, "motivo"] = motivo
    partidas.loc[i, "total_jogadas"] = len(tabuleiro.move_stack)

    partidas.to_csv(
        arquivo_partidas,
        index=False,
        encoding="utf-8"
    )

    versoes = {
        "brancas": partidas.loc[i, "versao_brancas"],
        "pretas": partidas.loc[i, "versao_pretas"]
    }

    for cor, versao in versoes.items():
        if not versao or versao.lower() == "humano":
            continue

        if resultado == "1/2-1/2":
            resultado_ia = "empate"
            pontos = 0.5
        elif (
            resultado == "1-0" and cor == "brancas"
        ) or (
            resultado == "0-1" and cor == "pretas"
        ):
            resultado_ia = "vitoria"
            pontos = 1
        else:
            resultado_ia = "derrota"
            pontos = 0

        desempenho = pd.DataFrame([{
            "partida_id": partida_id,
            "versao_ia": versao,
            "resultado": resultado_ia,
            "pontos": pontos
        }])

        desempenho.to_csv(
            arquivo_desempenho,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8"
        )

def resumo_desempenho(): # Retorna um resumo do desempenho das IAs em todas as partidas
    criar_arquivo(arquivo_desempenho, colunas_desempenho)

    dados = pd.read_csv(arquivo_desempenho)

    if dados.empty:
        return pd.DataFrame(columns=[
            "versao_ia",
            "partidas",
            "vitorias",
            "empates",
            "derrotas",
            "pontos",
            "aproveitamento"
        ])

    resumo = dados.groupby("versao_ia").agg(
        partidas=("partida_id", "count"),
        vitorias=("resultado", lambda x: (x == "vitoria").sum()),
        empates=("resultado", lambda x: (x == "empate").sum()),
        derrotas=("resultado", lambda x: (x == "derrota").sum()),
        pontos=("pontos", "sum")
    ).reset_index()

    resumo["aproveitamento"] = (
        resumo["pontos"] / resumo["partidas"] * 100
    ).round(2)

    return resumo

def ler_dados(): # Lê os dados do arquivo CSV e retorna um DataFrame
    criar_arquivo()
    return pd.read_csv(arquivo)
