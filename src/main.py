from service import AudioService
from database import TranscriptionRepository

service = AudioService()
repo = TranscriptionRepository()

def lambda_handler(event, _context):
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if not key.endswith(('.mp3', '.wav', '.m4a')):
            continue

        try:
            print(f"Processando: {key}")
            texto_transcrito = service.process_audio(bucket, key)
            repo.save(key, texto_transcrito)
            print(f"Sucesso: {key}")

        except Exception as e:
            print(f"Erro no arquivo {key}: {e}")
            raise e

    return {'statusCode': 200, 'body': 'Processado'}