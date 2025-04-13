import json
import os

def get_json_as_string(filepath: str) -> str:
    """
    Lê um arquivo JSON em `filepath` e retorna o conteúdo como string.
    Levanta FileNotFoundError se o arquivo não existir.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    
    json_str = json.dumps(data, ensure_ascii=False)  
    return json_str
