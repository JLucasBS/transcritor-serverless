import whisper
import boto3
import os
import uuid

class AudioService:
    def __init__(self):
        print("Carregando modelo...")
        self.model = whisper.load_model("base")
        self.s3 = boto3.client('s3')

    def process_audio(self, bucket, key):
        temp_path = f"/tmp/{uuid.uuid4()}_{os.path.basename(key)}"
        
        try:
            self.s3.download_file(bucket, key, temp_path)
            
            result = self.model.transcribe(temp_path)
            return result["text"].strip()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)