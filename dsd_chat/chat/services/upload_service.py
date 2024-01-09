import os
import requests
import dotenv
from typing import Optional

dotenv.load_dotenv()


def upload_document(document: str) -> Optional[str]:
    mq_url = os.environ['QSTASH_URL']
    worker_url = os.environ['WORKER_URL']
    qstash_token = os.environ['QSTASH_TOKEN']
    
    url = f'{mq_url}{worker_url}'
    data = {'text': document}
    headers = {'Authorization': f'Bearer {qstash_token}'}
    
    response = requests.post(url=url, data=data, headers=headers)
    if response.status_code != 200: return None
    
    body = response.json()
    return body['messageId']

def upsert_document(document: str) -> None:
    pass