import time
import pandas as pd
from jobspy import scrape_jobs


termos_it = [
        "Programador",
        "Desenvolvedor Software",
        "Engenheiro de Software",
        "Analista de Sistemas",
        "Suporte Técnico",
        "Administrador de Redes",
        "Cibersegurança"
]


lista_dataframes = []

print("A iniciar a pesquisa de vagas de IT em Angola...")


for cargo in termos_it:
    print(f"A pesquisar por: {cargo}...")
    try:
        
        vagas = scrape_jobs(
            site_name=["linkedin", "glassdoor"],
            search_term=cargo,  
            location="Angola",                
            results_wanted=15, 
            hours_old=168,                               
        )
        
        if not vagas.empty:
            lista_dataframes.append(vagas)
            print(f"-> Encontradas {len(vagas)} vagas para {cargo}.")
        else:
            print(f"-> Nenhuma vaga recente para {cargo}")
            
    except Exception as e:
        print(f"Erro ao pesquisar {cargo}: {e}")
    
    
    time.sleep(5)


if lista_dataframes:
    todos_os_trabalhos = pd.concat(lista_dataframes, ignore_index=True)
    
   
    todos_os_trabalhos = todos_os_trabalhos.drop_duplicates(subset=['id'])
    
  
    todos_os_trabalhos.to_csv("vagas_brutas_angola.csv", index=False)
    print(f"\nSucesso! {len(todos_os_trabalhos)} vagas únicas guardadas em 'vagas_brutas_angola.csv'.")
    

    print("\nPrimeiros resultados encontrados:")
    print(todos_os_trabalhos[['title', 'company', 'location', 'job_url']].head())
else:
    print("\nNenhuma vaga foi encontrada nos últimos 3 dias.")
