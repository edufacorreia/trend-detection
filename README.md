# TrendScout Engine 🚀

**TrendScout** é uma infraestrutura de Engenharia de Dados desenvolvida para monitorar, extrair e classificar tendências em redes sociais (Instagram/TikTok). O foco do projeto é transformar dados brutos de interações em inteligência de mercado, diferenciando modismos passageiros (*Fads*) de mudanças comportamentais consistentes (*Trends*).

## 🛠️ Tecnologias e Ferramentas
*   **Python 3.10+**: Linguagem base para o desenvolvimento da pipeline.
*   **Pandas**: Biblioteca padrão para manipulação e estruturação de dados.
*   **Instaloader**: Engine de extração de dados e interação com a plataforma.
*   **Python-Dotenv**: Gestão de variáveis de ambiente e segurança de credenciais.

## 🏛️ Padrões de Indústria Aplicados
Este repositório segue rigorosos princípios de engenharia de software utilizados em ambientes de produção:
*   **Google Style Docstrings**: Documentação técnica padronizada e legível por máquinas.
*   **Type Hinting**: Garantia de integridade de dados e facilidade de manutenção.
*   **Session Persistence**: Estratégia de bypass de mecanismos anti-bot e suporte nativo a 2FA.
*   **Security-First**: Isolamento de credenciais e política de exclusão de dados sensíveis via `.gitignore`.

## ⚙️ Configuração Inicial

1.  **Instale as dependências:**
    ```bash
    pip install instaloader pandas python-dotenv
    ```

2.  **Configure suas credenciais:**
    Crie um arquivo `.env` na raiz do projeto (nunca comite este arquivo!):
    ```env
    IG_USER=seu_usuario
    IG_PASS=sua_senha
    ```

3.  **Gestão de 2FA (Autenticação de Dois Fatores):**
    Caso sua conta possua 2FA ativo, gere o arquivo de sessão manualmente no terminal:
    ```bash
    instaloader --login seu_usuario
    ```

## 📖 Como Usar

Abaixo, um exemplo de implementação da camada de ingestão no seu script principal:

```python
import os
from dotenv import load_dotenv
from funcoes import extrai_dados_post_ig

# Lendo o arquivo secreto .env onde estão as senhas
# Carregamento de Environment Variables para gestão segura de segredos (Secrets Management)
load_dotenv()

# Buscando o usuário e senha do sistema com segurança
# Recuperação de credenciais via variáveis de ambiente para evitar Hardcoding de senhas
USER = os.getenv("IG_USER")
PASS = os.getenv("IG_PASS")
URL = "[https://www.instagram.com/p/CXYZ12345/](https://www.instagram.com/p/CXYZ12345/)"

# Rodando a função principal e guardando o resultado em uma tabela (DataFrame)
# Execução da pipeline de ingestão de dados com retorno de objeto estruturado (Pandas DF)
df_final = extrai_dados_post_ig(URL, USER, PASS)

# Exibindo as primeiras linhas para validar a extração
# Inspeção de sanidade dos dados coletados (Data Validation/Discovery)
print(df_final.head())
```

## 📂 Estrutura do Projeto

├── dados/               # Armazenamento de arquivos CSV (Raw Data Layer)
├── .env                 # Credenciais sensíveis (Ignorado pelo Controle de Versão)
├── .gitignore           # Definição de arquivos e pastas excluídos do rastreamento
├── funcoes.py           # Core Engine: Lógica de extração e tratamento de dados
├── main.ipynb           # Interface de execução e análise exploratória
└── README.md            # Documentação técnica do projeto
