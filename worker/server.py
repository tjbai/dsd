#!./venv/bin/python3

import os
import sys
import json
import dotenv
import backoff
import requests
from time import sleep
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from embed import chunk, embed, EmbeddedDocument

dotenv.load_dotenv()


port = 8001 if len(sys.argv) == 1 else int(sys.argv[1])
callback_url = os.environ['SERVER_URL']

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        sleep(1)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'heard')
        
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def _callback(self, data): requests.post(url=callback_url, data=data)
        
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            chunk_list = chunk(post_data['text'])
            doc: EmbeddedDocument = embed(chunk_list)
            serialized_doc = doc.serialize()
            
            self.send_response(200)
            self.end_headers()
            
            self._callback(serialized_doc)
            
        except KeyError as e:
            self.send_error(400, f'Incomplete body: {e}')
            
        except Exception as e:
            self._callback(EmbeddedDocument(embedded_successfully=False, chunk_list=None).serialize())
    
with ThreadingHTTPServer(('', port), Handler) as server:
    print(f'listening on port {port}')
    server.serve_forever()