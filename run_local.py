# run_local.py
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import lambda_handler

fake_event = {
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "NOME-DO-SEU-BUCKET-REAL-AQUI" 
        },
        "object": {
          "key": "pasta/teste.mp3" 
        }
      }
    }
  ]
}

class FakeContext:
    def get_remaining_time_in_millis(self):
        return 900000

if __name__ == "__main__":
    print("--- Iniciando Teste Local ---")
    
    try:
        response = lambda_handler(fake_event, FakeContext())
        
        print("\n--- Resultado ---")
        print(response)
        print("Verifique seu banco de dados local, a tabela deve ter sido criada e o dado inserido.")
        
    except Exception as e:
        print(f"\nErro no teste: {e}")