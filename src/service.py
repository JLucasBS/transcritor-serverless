import whisper
import boto3
import os
import uuid

class AudioService:
    def __init__(self):
        print("Carregando modelo...")
        self.model = whisper.load_model("base")
        self.s3 = boto3.client('s3')

    def _transcribe_core(self, file_path):
        result = self.model.transcribe(
            file_path, 
            language="pt", 
            task="transcribe"
        )
        return result["text"].strip()

    def process_s3_audio(self, bucket, key):
        temp_path = f"/tmp/{uuid.uuid4()}_{os.path.basename(key)}"
        
        try:
            self.s3.download_file(bucket, key, temp_path)
            return self._transcribe_core(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def process_local_audio(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        return self._transcribe_core(file_path)