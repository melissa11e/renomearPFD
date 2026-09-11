#le csv e começa na linha 1

import os
import pandas as pd
import re

# ==== CONFIGURAÇÕES ====
pasta_pdfs = r"C:\Users\melissa.lemes\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Área de Trabalho\subir"
arquivo_csv = r"C:\Users\melissa.lemes\Downloads\rhfp0774_185165 (3).csv"
# ==== LER CSV ====
df = pd.read_csv(arquivo_csv, sep=";", encoding="latin1")  # se for ; troque para sep=";"

# Garantir que são strings
df["MATRICULA"] = df["MATRICULA"].astype(str)

# Limpar CPF (remove tudo que não é número)
df["CPF"] = df["CPF"].astype(str).apply(lambda x: re.sub(r"\D", "", x))

# Criar dicionário: matricula -> cpf
mapa = dict(zip(df["MATRICULA"], df["CPF"]))

# ==== PROCESSAR PDFs ====
for arquivo in os.listdir(pasta_pdfs):
    if arquivo.lower().endswith(".pdf"):
        
        match = re.match(r"(\d+)_", arquivo)
        
        if match:
            matricula = match.group(1)
            
            if matricula in mapa:
                cpf = mapa[matricula]
                
                novo_nome = f"{matricula}_{cpf}.pdf"
                
                caminho_antigo = os.path.join(pasta_pdfs, arquivo)
                caminho_novo = os.path.join(pasta_pdfs, novo_nome)
                
                if not os.path.exists(caminho_novo):
                    os.rename(caminho_antigo, caminho_novo)
                    print(f"✅ {arquivo} -> {novo_nome}")
                else:
                    print(f"⚠ Já existe: {novo_nome}")
            else:
                print(f"❌ Matrícula não encontrada: {matricula}")