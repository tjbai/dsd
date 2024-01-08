import json
from typing import List
from dataclasses import dataclass, asdict


type Chunk = str

@dataclass
class EmbeddedDocument:
    chunks: List[Chunk]
    embeddings: List[List[float]]
    
    def serialize(self): return json.dumps(asdict(self)).encode('utf-8')

def chunk(document: str) -> List[Chunk]:
    return []

def embed(chunk_list: List[Chunk]) -> EmbeddedDocument:
    return EmbeddedDocument(['a', 'b', 'c'], [[1,2,3], [4,5,6]])