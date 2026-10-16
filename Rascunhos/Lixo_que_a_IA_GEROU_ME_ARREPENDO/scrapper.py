import time
import pandas as pd
from jobspy import scrape_jobs

def executar_scraping_vagas(termos_busca, localizacao="Angola", results_wanted=15, hours_old=72):
    """
    Scraper formal de vagas (LinkedIn, Glassdoor) usando os termos 
    gerados pelo Agente ou passados pelo utilizador.
    """
    lista_dataframes = []
    print(f"[*] A iniciar pesquisa de vagas formais em: {localizacao}")

    for cargo in termos_busca:
        print(f"  -> Pesquisando por: {cargo}...")
        try:
            vagas = scrape_jobs(
                site_name=["linkedin", "glassdoor"],
                search_term=cargo,
                location=localizacao,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed='angola'
            )
            if vagas is not None and not vagas.empty:
                lista_dataframes.append(vagas)
        except Exception as e:
            print(f"  [!] Erro ao pesquisar {cargo}: {e}")
        
        time.sleep(2.5)  # Intervalo de segurança anti-bloqueio

    if lista_dataframes:
        todos = pd.concat(lista_dataframes, ignore_index=True)
        if 'id' in todos.columns:
            todos = todos.drop_duplicates(subset=['id'])
        else:
            todos = todos.drop_duplicates(subset=['title', 'company'])
        todos = todos.fillna("")
        todos.to_csv("vagas_angola_raw.csv", index=False)
        return todos
    
    return pd.DataFrame()

def executar_scraping_publicacoes(termos_post, localizacao="Angola", hours_old=168):
    """
    Scraper para capturar anúncios informais e publicações de recrutamento 
    (últimos 7 dias = 168 horas).
    """
    lista_dfs = []
    print(f"[*] A monitorizar publicações informais em: {localizacao} (últimos 7 dias)")

    for termo in termos_post:
        print(f"  -> Monitorizando expressão/tag: {termo}...")
        try:
            # Pesquisa com foco em publicações de feed e alertas
            posts = scrape_jobs(
                site_name=["linkedin"],
                search_term=termo,
                location=localizacao,
                results_wanted=10,
                hours_old=hours_old,
            )
            if posts is not None and not posts.empty:
                lista_dfs.append(posts)
        except Exception as e:
            print(f"  [!] Erro ao monitorizar posts para {termo}: {e}")
        
        time.sleep(2.0)

    if lista_dfs:
        df_posts = pd.concat(lista_dfs, ignore_index=True)
        if 'id' in df_posts.columns:
            df_posts = df_posts.drop_duplicates(subset=['id'])
        df_posts = df_posts.fillna("")
        df_posts.to_csv("publicacoes_raw.csv", index=False)
        return df_posts

    return pd.DataFrame()