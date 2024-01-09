import json
from typing import List, Optional
from dataclasses import dataclass, asdict

import dotenv
import openai
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv.load_dotenv()
client = openai.OpenAI()

type RawChunk = str

@dataclass
class Chunk:
    index: int
    chunk: str
    summary: str
    embedding: List[float]
    
@dataclass
class EmbeddedDocument:
    embedded_successfully: bool
    chunk_list: Optional[List[Chunk]]    
    def serialize(self): return json.dumps(asdict(self)).encode('utf-8')

# TODO -- can we do this with no dependencies?
def chunk(document: str) -> List[RawChunk]:
    tokenizer = tiktoken.get_encoding('cl100k_base')
    
    def chunk_length(raw_chunk: str): return len(tokenizer.encode(raw_chunk))

    # TODO -- hyperparameters!
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=256,
        length_function=chunk_length,
    )
    
    return splitter.split_text(document)

def summarize(chunk_list: List[RawChunk], model: str = 'gpt-3.5-turbo') -> List[str]:
    system_prompt = '''You are a helpful assistant that summarizes pieces of text.
    Generate a concise and informative summary (2-3 sentences) that adeptly 
    captures the key points and main ideas of the provided text. Maintain coherence and readability.
    If applicable, include any noteworth insights or context that would enhance the overall understanding.
    '''
    
    res = []
    for chunk in chunk_list:
        
        # TODO -- mess w this
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': chunk}
            ],
            temperature=0.0
        )
        
        res.append(response.choices[0].message.content)
        
    return res

def embed(chunk_list: List[RawChunk], model: str = 'text-embedding-ada-002') -> EmbeddedDocument:
    summary_list = summarize(chunk_list)
    embedding_list = client.embeddings.create(input=summary_list, model=model)
    
    return EmbeddedDocument(
        embedded_successfully=True,
        chunk_list=[
            Chunk(index=i, chunk=chunk, summary=summary, embedding=embedding)
            for i, (chunk, summary, embedding) in enumerate(zip(chunk_list, summary_list, embedding_list))
            ]
        )