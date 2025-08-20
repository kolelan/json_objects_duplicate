import json
from typing import List, Dict, Any, Tuple
from config.settings import NAME_FIELD, DESC_FIELD, COMPACT_JSON
from .validator import is_cyrillic, is_latin, detect_object_structure, normalize_object

def load_json_data(file_path: str) -> Tuple[List[Any], List[str]]:
    """Загружает JSON данные и определяет структуру объектов"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Ошибка при чтении файла: {e}")

    if not isinstance(data, list):
        raise Exception("JSON должен содержать массив объектов")

    # Определяем структуру данных
    structure_types = []
    for item in data:
        structure_types.append(detect_object_structure(item))

    return data, structure_types

def sort_data_by_name(data: List[Any], structure_types: List[str]) -> Tuple[List[Any], List[str]]:
    """Сортирует данные по полю name или ключу"""
    # Создаем список кортежей (ключ_сортировки, объект, тип_структуры)
    sort_keys = []

    for i, (item, structure_type) in enumerate(zip(data, structure_types)):
        if structure_type == "standard":
            sort_key = item.get("name", "")
        elif structure_type == "key_value":
            sort_key = list(item.keys())[0] if item else ""
        else:
            sort_key = ""
        sort_keys.append((sort_key, i, item, structure_type))

    # Сортируем по ключу
    sort_keys.sort(key=lambda x: x[0])

    # Восстанавливаем отсортированные данные
    sorted_data = [item for _, _, item, _ in sort_keys]
    sorted_structure_types = [struct_type for _, _, _, struct_type in sort_keys]

    return sorted_data, sorted_structure_types

def process_duplicates(data: List[Any], structure_types: List[str], keep_first: bool = False) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
    """Обрабатывает дубликаты в данных"""
    # Сортируем данные по name/key
    sorted_data, sorted_structure_types = sort_data_by_name(data, structure_types)

    normalized_data = []
    line_numbers = {}

    # Нормализуем данные и запоминаем номера строк (после сортировки)
    for i, (item, structure_type) in enumerate(zip(sorted_data, sorted_structure_types), 1):
        normalized = normalize_object(item, structure_type)
        normalized_data.append(normalized)

        name = normalized["name"]
        if name not in line_numbers:
            line_numbers[name] = []
        line_numbers[name].append(i)

    # Группируем по имени
    name_groups = {}
    for i, item in enumerate(normalized_data):
        name = item["name"]
        if name not in name_groups:
            name_groups[name] = []
        name_groups[name].append((i, item))

    result = []
    report_data = []

    for name, items in name_groups.items():
        if len(items) == 1:
            # Только один объект
            result.append(items[0][1])
        else:
            # Несколько объектов с одинаковым name
            indices = [idx for idx, _ in items]
            objects = [obj for _, obj in items]

            if keep_first:
                # Режим "оставлять первый"
                result.append(objects[0])
                for i in range(1, len(objects)):
                    report_data.append({
                        'line': line_numbers[name][i],
                        'name': name,
                        'desc': objects[i]["desc"],
                        'object': sorted_data[indices[i]]
                    })
            else:
                # Стандартная логика обработки
                valid_objects = []
                invalid_objects = []

                for idx, obj in items:
                    desc = obj["desc"]
                    if desc and desc.strip():
                        valid_objects.append((idx, obj))
                    else:
                        invalid_objects.append((idx, obj))

                if len(valid_objects) == 0:
                    # Нет объектов с заполненным desc
                    result.append(objects[0])
                    for i in range(1, len(objects)):
                        report_data.append({
                            'line': line_numbers[name][i],
                            'name': name,
                            'desc': objects[i]["desc"],
                            'object': sorted_data[indices[i]]
                        })
                elif len(valid_objects) == 1:
                    # Один объект с заполненным desc
                    result.append(valid_objects[0][1])
                    for idx, obj in invalid_objects:
                        report_data.append({
                            'line': line_numbers[name][indices.index(idx)],
                            'name': name,
                            'desc': obj["desc"],
                            'object': sorted_data[idx]
                        })
                else:
                    # Несколько объектов с заполненным desc
                    cyrillic_objects = []
                    latin_objects = []
                    other_objects = []

                    for idx, obj in valid_objects:
                        desc = obj["desc"]
                        if is_cyrillic(desc):
                            cyrillic_objects.append((idx, obj))
                        elif is_latin(desc):
                            latin_objects.append((idx, obj))
                        else:
                            other_objects.append((idx, obj))

                    if cyrillic_objects:
                        # Берем первый кириллический
                        result.append(cyrillic_objects[0][1])
                        for idx, obj in cyrillic_objects[1:] + latin_objects + other_objects:
                            report_data.append({
                                'line': line_numbers[name][indices.index(idx)],
                                'name': name,
                                'desc': obj["desc"],
                                'object': sorted_data[idx]
                            })
                    elif latin_objects:
                        # Берем первый латинский
                        result.append(latin_objects[0][1])
                        for idx, obj in latin_objects[1:] + other_objects:
                            report_data.append({
                                'line': line_numbers[name][indices.index(idx)],
                                'name': name,
                                'desc': obj["desc"],
                                'object': sorted_data[idx]
                            })
                    else:
                        # Берем первый из других
                        result.append(other_objects[0][1])
                        for idx, obj in other_objects[1:]:
                            report_data.append({
                                'line': line_numbers[name][indices.index(idx)],
                                'name': name,
                                'desc': obj["desc"],
                                'object': sorted_data[idx]
                            })

                    # Добавляем invalid objects
                    for idx, obj in invalid_objects:
                        report_data.append({
                            'line': line_numbers[name][indices.index(idx)],
                            'name': name,
                            'desc': obj["desc"],
                            'object': sorted_data[idx]
                        })

    return result, report_data