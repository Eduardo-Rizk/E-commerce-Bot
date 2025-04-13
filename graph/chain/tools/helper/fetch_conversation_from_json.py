import json
import os
from typing import List
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage


def fetch_conversation_from_json(filepath: str) -> List[BaseMessage]:
    """
    Lê um arquivo JSON contendo o histórico de conversas (mock)
    e retorna uma lista de mensagens do tipo HumanMessage, AIMessage etc.
    
    Formato esperado no JSON:
    [
      {"role": "user", "content": "texto..."},
      {"role": "assistant", "content": "texto..."}
    ]
    """
    if not os.path.exists(filepath):
        print(f"[fetch_conversation_from_json] Arquivo não existe: {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages: List[BaseMessage] = []
    for item in data:
        role = item.get("role", "").lower()
        content = item.get("content", "")

        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role in ("assistant", "ai"):
            messages.append(AIMessage(content=content))
        else:
            # Caso queira descartar ou logar:
            print(f"[fetch_conversation_from_json] Role '{role}' não reconhecido, pulando.")
            continue

    return messages
