import os
import requests
import dotenv
from typing import Optional
import backoff

dotenv.load_dotenv()


@backoff.on_exception(backoff.expo, requests.RequestException)
def process_document(document: str) -> bool:
    
    '''
    # TODO -- in principle we want this to be async
    mq_url = os.environ['QSTASH_URL']
    worker_url = os.environ['WORKER_URL']
    qstash_token = os.environ['QSTASH_TOKEN']
    '''
    
    
    
    return True

def upsert_document(document: str) -> None:
    pass