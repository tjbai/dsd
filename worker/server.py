#!./venv/bin/python3

import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from embed import chunk, embed, EmbeddedDocument


port = 8001 if len(sys.argv) == 1 else int(sys.argv[1])

class Handler(BaseHTTPRequestHandler):
    
    def happy_response(self):
        self.send_response(200)
        self.end_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        print(f'{content_length}:{post_data}')
        
        try:
            chunk_list = chunk(post_data['text'])
            doc: EmbeddedDocument = embed(chunk_list)
            self.happy_response()
            self.wfile.write(doc.serialize())
        except KeyError as e: self.send_error(400, f'Incomplete body: {e}')
        except Exception as e: self.send_error(400, f'Unknown exception: {e}')
    
with HTTPServer(('', port), Handler) as server: server.serve_forever()