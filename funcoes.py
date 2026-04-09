import instaloader
import pandas as pd
import os
import time
import random
from typing import Optional

# Instanciando a classe principal sem parâmetros de controle de fluxo no construtor
L = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

# Configurando a propriedade de Rate Limiting pós-instanciação (Object Property Assignment)
L.sleep_between_interactions = True

def extrai_dados_post_ig(
    url_do_post: str, 
    username: str, 
    password: str, 
    salvar_csv: bool = True
) -> pd.DataFrame:
    """Extrai metadados e todos os comentários de um post do Instagram."""
    
    # Definição do diretório de Output para armazenamento de dados brutos (Raw/Bronze layer)
    FOLDER_NAME = "dados"
    
    # Inicialização da Engine de Scraping com Throttling nativo e User-Agent Spoofing
    L = instaloader.Instaloader(
        sleep_between_interactions=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    # Implementação de Session Persistence para bypass de desafios de Auth e 2FA
    try:
        L.load_session_from_file(username)
        print(f"✅ Sessão carregada via arquivo para: {username}")
    except FileNotFoundError:
        # Fallback para autenticação via Credenciais (User/Pass) com persistência de Token
        print(f"⚠️ Sessão local não encontrada. Tentando login por senha...")
        try:
            L.login(username, password)
            L.save_session_to_file()
            print(f"✅ Login efetuado e nova sessão salva.")
        except Exception as e:
            print(f"❌ Falha crítica na autenticação: {e}")
            return pd.DataFrame()

    try:
        # Extração e normalização do Shortcode para garantir integridade referencial
        shortcode = url_do_post.strip("/").split("/")[-1]
        print(f"🚀 Processando post: {shortcode}...")
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Schema Mapping dos metadados do Objeto Post para estrutura tabular
        post_info = {
            "post_id": post.shortcode,
            "autor": post.owner_username,
            "legenda": post.caption,
            "likes_post": post.likes,
            "comentarios_count": post.comments,
            "data_post_utc": post.date_utc
        }
        df_post = pd.DataFrame([post_info])

        # Iteração sobre geradores de comentários com parse para lista de objetos (JSON-like)
        comments_list = []
        for comment in post.get_comments():
            comments_list.append({
                "comment_id": comment.id,
                "usuario": comment.owner.username,
                "texto": comment.text,
                "likes_comentario": comment.likes,
                "data_comentario_utc": comment.created_at_utc,
                "post_id": shortcode
            })
            
            # Implementação de Rate Limiting dinâmico para mitigação de detecção Anti-Bot
            if len(comments_list) % 50 == 0:
                print(f"📦 {len(comments_list)} comentários coletados...")
                time.sleep(random.uniform(2, 5))

        df_comments = pd.DataFrame(comments_list)

        # FileSystem Persistence
        if salvar_csv and not df_comments.empty:
            if not os.path.exists(FOLDER_NAME):
                os.makedirs(FOLDER_NAME)
            
            p_path = os.path.join(FOLDER_NAME, f"post_{shortcode}_info.csv")
            c_path = os.path.join(FOLDER_NAME, f"post_{shortcode}_comentarios.csv")
            
            # Serialização em CSV utilizando UTF-8-BOM para compatibilidade cross-platform
            df_post.to_csv(p_path, index=False, encoding='utf-8-sig')
            df_comments.to_csv(c_path, index=False, encoding='utf-8-sig')
            print(f"💾 Dados salvos com sucesso em: {FOLDER_NAME}/")

        return df_comments

    except Exception as e:
        print(f"❌ Erro na extração de dados: {e}")
        return pd.DataFrame()