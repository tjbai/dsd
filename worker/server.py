#!./venv/bin/python3

import sys
import json
import requests
import backoff
from time import sleep
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from embed import chunk, embed, EmbeddedDocument


port = 8001 if len(sys.argv) == 1 else int(sys.argv[1])
callback_url = 'http://127.0.0.1/8000'

class Handler(BaseHTTPRequestHandler):
    
    def happy_response(self):
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        sleep(1)
        self.happy_response()
        self.wfile.write(b'heard')
        
    @backoff.on_exception(requests.exceptions.RequestException)
    def hit_callback(self, data): requests.post(url=callback_url, data=data)
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        print(f'{content_length}:{post_data}')
        
        try:
            chunk_list = chunk(post_data['text'])
            doc: EmbeddedDocument = embed(chunk_list)
            serialized_doc = doc.serialize()
            
            self.happy_response()
            self.wfile.write(serialized_doc)
            self.hit_callback(serialized_doc)
            
        except KeyError as e: self.send_error(400, f'Incomplete body: {e}')
        except Exception as e: self.send_error(400, f'Unknown exception: {e}')
    
with ThreadingHTTPServer(('', port), Handler) as server: server.serve_forever()