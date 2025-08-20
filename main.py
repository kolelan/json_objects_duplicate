#!/usr/bin/env python3
import argparse
from core.processor import load_json_data, process_duplicates
from core.reporter import generate_report, save_result
from config.settings import DEFAULT_OUTPUT_FILE, DEFAULT_REPORT_FILE


def main():
    parser = argparse.ArgumentParser(description='Обработка JSON файла с удалением дубликатов')
    parser.add_argument('input', help='Входной JSON файл')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT_FILE,
                        help=f'Выходной JSON файл (по умолчанию: {DEFAULT_OUTPUT_FILE})')
    parser.add_argument('-r', '--report', default=DEFAULT_REPORT_FILE,
                        help=f'Файл отчета (по умолчанию: {DEFAULT_REPORT_FILE})')
    parser.add_argument('-f', '--keep-first', action='store_true',
                        help='Всегда оставлять первый объект, удалять последующие')

    args = parser.parse_args()

    try:
        # Загружаем данные
        data, structure_types = load_json_data(args.input)

        # Обрабатываем дубликаты
        result, report_data = process_duplicates(data, structure_types, args.keep_first)

        # Сохраняем результаты
        save_result(result, args.output)
        generate_report(report_data, args.report)

    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())