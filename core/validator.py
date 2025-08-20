import re
from typing import Any, Dict
from config.settings import CYRILLIC_PATTERN, LATIN_PATTERN

def is_cyrillic(text: str) -> bool:
    """Проверяет, содержит ли текст только кириллические символы"""
    if not text or not isinstance(text, str):
        return False
    return bool(re.match(CYRILLIC_PATTERN, text))

def is_latin(text: str) -> bool:
    """Проверяет, содержит ли текст только латинские символы"""
    if not text or not isinstance(text, str):
        return False
    return bool(re.match(LATIN_PATTERN, text))

def detect_object_structure(obj: Any) -> str:
    """
    Определяет структуру объекта:
    - 'standard': {name: "", desc: ""}
    - 'key_value': {"key": "value"}
    - 'unknown': неизвестная структура
    """
    if isinstance(obj, dict):
        # Проверяем стандартную структуру
        if "name" in obj and "desc" in obj:
            return "standard"
        # Проверяем структуру ключ-значение
        elif len(obj) == 1:
            key = list(obj.keys())[0]
            value = obj[key]
            if isinstance(key, str) and isinstance(value, str):
                return "key_value"
    return "unknown"

def normalize_object(obj: Any, structure_type: str) -> Dict[str, str]:
    """Нормализует объект к стандартной структуре"""
    if structure_type == "standard":
        return {
            "name": obj.get("name", ""),
            "desc": obj.get("desc", "")
        }
    elif structure_type == "key_value":
        key = list(obj.keys())[0]
        return {
            "name": key,
            "desc": obj[key]
        }
    else:
        return {
            "name": "",
            "desc": ""
        }