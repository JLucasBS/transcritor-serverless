import sys
import os
from dotenv import load_dotenv

# 1. Carrega ambiente
load_dotenv()

# 2. Ajusta path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.service import AudioService
from src.database import TranscriptionRepository

ARQUIVO_LOCAL = r"C:\Users\jluca\Minhas Gravacoes\gravacao_1763063426205_chunk4.wav"

if __name__ == "__main__":
    print(f"--- Iniciando Teste Manual com arquivo: {ARQUIVO_LOCAL} ---")

    if not os.path.exists(ARQUIVO_LOCAL):
        print("❌ Erro: Coloque um arquivo .mp3 na raiz do projeto para testar.")
        sys.exit(1)

    try:
        service = AudioService()
        repo = TranscriptionRepository()

        print("Transcrevendo...")
        texto = service.process_local_audio(ARQUIVO_LOCAL)
        print(f"Texto extraído: {texto[:50]}...")

        print("Salvando no banco...")
        repo.save(f"LOCAL_{os.path.basename(ARQUIVO_LOCAL)}", texto)
        
        print("✅ Sucesso! Verifique o banco de dados.")

    except Exception as e:
        print(f"❌ Erro: {e}")