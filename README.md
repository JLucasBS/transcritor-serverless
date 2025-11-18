# Transcritor Serverless (AWS Lambda + Whisper)

Este projeto é uma função **AWS Lambda** containerizada que transcreve automaticamente arquivos de áudio enviados para um bucket **S3** usando o modelo **OpenAI Whisper**. O resultado da transcrição é salvo em um banco de dados **PostgreSQL**.

## 🚀 Arquitetura

1.  **Upload:** Arquivo `.mp3` é enviado para o Bucket S3.
2.  **Trigger:** Evento S3 aciona a Lambda.
3.  **Processamento:**
    -   Download do áudio para `/tmp`.
    -   Transcrição via `openai-whisper`.
    -   Salvamento do texto no PostgreSQL.
4.  **Clean Up:** Remoção do arquivo temporário.

## 🛠️ Tecnologias

-   Python 3.10
-   AWS Lambda (Container Image)
-   OpenAI Whisper (Modelo 'base')
-   PostgreSQL (Armazenamento)
-   Docker & Docker Compose

---

## ⚙️ Configuração Local (Para Desenvolvimento)

### Pré-requisitos

-   Docker e Docker Compose instalados.
-   Python 3.10+ instalado.
-   **FFmpeg** instalado no sistema (necessário para o Whisper rodar localmente).
    -   _Ubuntu:_ `sudo apt install ffmpeg`
    -   _Windows:_ Instalar via Chocolatey ou baixar o executável e adicionar ao PATH.

### 1. Instalar Dependências

Recomenda-se usar um ambiente virtual (`venv`).

```bash
pip install -r requirements.txt
```

### 2. Subir Banco de Dados Local

Use o Docker Compose para subir uma instância Postgres isolada.

```bash
docker-compose up -d
```

### 3. Configurar Variáveis de Ambiente

Para rodar localmente, você precisa exportar as variáveis no seu terminal (ou criar um arquivo `.env`).

#### Linux/Mac

```bash
export DB_HOST=localhost
export DB_NAME=db_transcricao
export DB_USER=user_teste
export DB_PASS=password_teste
export AWS_PROFILE=default  # Ou suas chaves AWS_ACCESS_KEY_ID...
```

#### Windows (PowerShell)

```
$env:DB_HOST="localhost"
$env:DB_NAME="db_transcricao"
$env:DB_USER="user_teste"
$env:DB_PASS="password_teste"
# Configure suas credenciais AWS via 'aws configure' ou variáveis manuais
```

### 4. Executar Teste

Execute o script simulador que finge ser um evento do S3. Nota: Você precisa ter um arquivo real no seu S3 para isso funcionar.

```bash
python run_local.py
```

## ☁️ Deploy na AWS

Como o pacote do Whisper + PyTorch é grande, usamos Docker Image em vez de arquivo .zip.

### 1. Login no ECR (Elastic Container Registry)

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ID_DA_SUA_CONTA>.dkr.ecr.us-east-1.amazonaws.com
```

### 2. Build e Push da Imagem

```bash
# Build
docker build -t transcritor-whisper .

# Tag (Substitua pela URI do seu repositório ECR)
docker tag transcritor-whisper:latest <ID_DA_SUA_CONTA>[.dkr.ecr.us-east-1.amazonaws.com/transcritor-whisper:latest](https://.dkr.ecr.us-east-1.amazonaws.com/transcritor-whisper:latest)

# Push
docker push <ID_DA_SUA_CONTA>[.dkr.ecr.us-east-1.amazonaws.com/transcritor-whisper:latest](https://.dkr.ecr.us-east-1.amazonaws.com/transcritor-whisper:latest)
```

### 3. Configuração da Lambda

1. Crie uma nova função Lambda selecionando Container Image.
2. Aponte para a imagem no ECR.
3. Configurações Essenciais:
    - Memory: Min 2048MB (Recomendado 4GB).
    - Timeout: Aumente para 5 a 10 minutos.
    - Environment Variables: Configure DB_HOST, DB_PASS, etc. (Aponte para seu RDS ou Supabase).
4. Adicione a permissão S3 Read na Role da Lambda.
5. Configure o S3 Trigger no bucket desejado.

---

## 📂 Estrutura do Projeto

```Plaintext
transcritor-serverless/
│
├── src/                      # Código Fonte da Aplicação
│   ├── __init__.py           # (Opcional) Marca a pasta como pacote Python
│   ├── main.py               # O Handler (Ponto de entrada da Lambda)
│   ├── service.py            # Lógica de Negócio (Whisper + S3)
│   └── database.py           # Acesso a Dados (Conexão Postgres)
│
├── Dockerfile                # Definição da Imagem para o AWS Lambda
├── requirements.txt          # Lista de bibliotecas (whisper, boto3, psycopg2...)
├── docker-compose.yml        # Configuração do Postgres local para testes
├── run_local.py              # Script que simula o evento da AWS localmente
├── README.md                 # Documentação do projeto
└── .gitignore                # Arquivos que o Git deve ignorar
```
