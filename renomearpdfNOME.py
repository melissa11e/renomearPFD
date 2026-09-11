#le csv e começa na linha 1

import os
import pandas as pd
import re

# ==== CONFIGURAÇÕES ====
pasta_pdfs = r
arquivo_csv = r
# ==== LER CSV ====
df = pd.read_csv(arquivo_csv, sep=";", encoding="latin1")

# Garantir que são strings
df["MATRICULA"] = df["MATRICULA"].astype(str)
df["CPF"] = df["CPF"].astype(str).apply(lambda x: re.sub(r"\D", "", x))
df["NOME_COMPLETO"] = df["NOME_COMPLETO"].astype(str).str.strip()

# Criar dicionário: nome -> (cpf, matricula)
mapa = {
    nome.upper(): (cpf, matricula)
    for nome, cpf, matricula in zip(
        df["NOME_COMPLETO"],
        df["CPF"],
        df["MATRICULA"]
    )
}

# ==== PROCESSAR PDFs ====
for arquivo in os.listdir(pasta_pdfs):
    if arquivo.lower().endswith(".pdf"):

        nome_pdf = os.path.splitext(arquivo)[0].strip().upper()

        if nome_pdf in mapa:
            cpf, matricula = mapa[nome_pdf]

            novo_nome = f"{cpf}_{matricula}.pdf"

            caminho_antigo = os.path.join(pasta_pdfs, arquivo)
            caminho_novo = os.path.join(pasta_pdfs, novo_nome)

            if not os.path.exists(caminho_novo):
                os.rename(caminho_antigo, caminho_novo)
                print(f"✅ {arquivo} -> {novo_nome}")
            else:
                print(f"⚠ Já existe: {novo_nome}")
        else:
            print(f"❌ Nome não encontrado: {nome_pdf}")
