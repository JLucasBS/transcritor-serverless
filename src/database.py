import os
import psycopg2
from datetime import datetime

class TranscriptionRepository:
    def __init__(self):
        self.conn_str = f"host={os.getenv('DB_HOST')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')} port={os.getenv('DB_PORT', '5432')}"
        
        self._ensure_table_exists()

    def _get_connection(self):
        return psycopg2.connect(self.conn_str)

    def _ensure_table_exists(self):
        ddl_query = """
            CREATE TABLE IF NOT EXISTS transcricoes (
                id SERIAL PRIMARY KEY,
                nome_arquivo VARCHAR(255) NOT NULL,
                texto TEXT,
                data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(ddl_query)
                conn.commit()
        except Exception as e:
            print(f"Erro ao verificar/criar tabela: {e}")
            raise e

    def save(self, filename: str, text: str):
        sql = """
            INSERT INTO transcricoes (nome_arquivo, texto, data_processamento) 
            VALUES (%s, %s, %s)
        """
        
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (filename, text, datetime.now()))
            conn.commit()