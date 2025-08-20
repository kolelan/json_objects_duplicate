import json
from typing import List, Dict, Any
from config.settings import DEFAULT_REPORT_FILE, DEFAULT_OUTPUT_FILE, COMPACT_JSON

def generate_report(report_data: List[Dict[str, Any]], report_file: str = None) -> None:
    """Генерирует отчет о дубликатах"""
    if report_file is None:
        report_file = DEFAULT_REPORT_FILE

    if not report_data:
        print("Дубликатов не найдено, отчет не создан.")
        return

    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Line\tName\tDesc\n")
            for item in report_data:
                f.write(f"{item['line']}\t{item['name']}\t{item['desc']}\n")
        print(f"Отчет сохранен в файл: {report_file}")
    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")

def save_result(data: List[Dict[str, str]], output_file: str = None) -> None:
    """Сохраняет результат обработки в компактном формате"""
    if output_file is None:
        output_file = DEFAULT_OUTPUT_FILE

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if COMPACT_JSON:
                # Компактный формат: каждый объект в одной строке
                f.write('[\n')
                for i, item in enumerate(data):
                    line = json.dumps(item, ensure_ascii=False)
                    if i < len(data) - 1:
                        line += ','
                    f.write(f'  {line}\n')
                f.write(']\n')
            else:
                # Стандартное форматирование
                json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Результат сохранен в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")