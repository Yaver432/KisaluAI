import os
import json
import pandas as pd
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analisar_vaga_com_ia(titulo, empresa, descricao):
    prompt_sistema = """
    És um assistente especialista em Inteligência de Mercado e RH. 
    Analisa a descrição da vaga fornecida. O teu objetivo é extrair os dados, mesmo que a descrição seja curta. 
    Define SEMPRE "e_vaga_valida" como true, a menos que o texto seja spam óbvio ou irrelevante.
    Devolve obrigatoriamente um objeto JSON puro com a seguinte estrutura:
    {
        "e_vaga_valida": true,
        "cargo_limpo": "Nome limpo do cargo",
        "requisitos_principais": ["requisito 1", "requisito 2"],
        "resumo_executivo": "Resumo curto da vaga."
    }
    """
    
    try:

        chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Título: {titulo}\nEmpresa: {empresa}\nDescrição: {descricao}"}
                    ],
                    model="openai/gpt-oss-120b", 
                    response_format={"type": "json_object"}
                )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"  [!] Erro ao comunicar com a IA: {e}")
        return None

def main():
    csv_filename = "vagas_brutas_angola.csv"
    
    print(f"=== A LER DADOS DE '{csv_filename}' ===")
    
    if not os.path.exists(csv_filename):
        print(f"[!] Ficheiro '{csv_filename}' não encontrado. Corre primeiro o scraper!")
        return

    df = pd.read_csv(csv_filename)
    df = df.fillna("")
    
    if df.empty:
        print("[!] O ficheiro CSV está vazio.")
        return

    print(f"[+] {len(df)} vagas encontradas no ficheiro. A processar com a IA da Groq...\n")
    print("=" * 60)

    vagas_por_empresa = {}

    for index, row in df.iterrows():
        titulo = row.get('title', 'N/A')
        empresa = row.get('company', 'Empresa Desconhecida')
        local = row.get('location', 'Angola')
        link = row.get('job_url', 'N/A')
        descricao = row.get('description', '')

        print(f"[*] A analisar: [{empresa}] {titulo}...")
        

        analise = analisar_vaga_com_ia(titulo, empresa, descricao)

        print(f"    [DEBUG] Resposta da IA: {analise}")
        
        if analise and analise.get("e_vaga_valida"):

            item_vaga = {
                "titulo_original": titulo,
                "cargo_limpo": analise.get("cargo_limpo", titulo),
                "localizacao": local,
                "link": link,
                "requisitos": analise.get("requisitos_principais", []),
                "resumo": analise.get("resumo_executivo", "")
            }
            

            if empresa not in vagas_por_empresa:
                vagas_por_empresa[empresa] = []
            vagas_por_empresa[empresa].append(item_vaga)

    print("\n" + "=" * 60)
    print("                 RELATÓRIO DE VAGAS POR EMPRESA")
    print("=" * 60 + "\n")

    for empresa, lista_vagas in vagas_por_empresa.items():
        print(f"EMPRESA: {empresa.upper()} ({len(lista_vagas)} vaga(s))")
        print("-" * 50)
        
        for i, vaga in enumerate(lista_vagas, 1):
            print(f"  {i}. Cargo: {vaga['cargo_limpo']}")
            print(f"     Local: {vaga['localizacao']}")
            print(f"     Resumo: {vaga['resumo']}")
            print(f"     Requisitos: {', '.join(vaga['requisitos'])}")
            print(f"     Link: {vaga['link']}")
            print("")
        print("=" * 50 + "\n")

  
    with open("relatorio_rh_final.json", "w", encoding="utf-8") as f:
        json.dump(vagas_por_empresa, f, ensure_ascii=False, indent=4)
        
    print("[CONCLUÍDO] Relatório agrupado guardado com sucesso em 'relatorio_rh_final.json'!")

if __name__ == "__main__":
    main()