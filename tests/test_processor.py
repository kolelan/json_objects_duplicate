import unittest
import json
import os
from core.processor import load_json_data, process_duplicates, sort_data_by_name

class TestProcessor(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.standard_data = [
            {"name": "z_test", "desc": "описание z"},
            {"name": "a_test", "desc": "description a"},
            {"name": "m_test", "desc": ""},
            {"name": "b_test", "desc": "описание b кириллица"}
        ]

        self.key_value_data = [
            {"z_key": "value z"},
            {"a_key": "value a"},
            {"m_key": ""},
            {"b_key": "value b"}
        ]

        # Сохраняем тестовые файлы
        with open('test_std.json', 'w', encoding='utf-8') as f:
            json.dump(self.standard_data, f)

        with open('test_kv.json', 'w', encoding='utf-8') as f:
            json.dump(self.key_value_data, f)

    def tearDown(self):
        # Удаляем тестовые файлы
        if os.path.exists('test_std.json'):
            os.remove('test_std.json')
        if os.path.exists('test_kv.json'):
            os.remove('test_kv.json')

    def test_sort_data_by_name_standard(self):
        """Тест сортировки стандартных данных"""
        structure_types = ['standard'] * 4
        sorted_data, sorted_types = sort_data_by_name(self.standard_data, structure_types)

        # Проверяем порядок сортировки
        names = [item['name'] for item in sorted_data]
        self.assertEqual(names, ['a_test', 'b_test', 'm_test', 'z_test'])

        # Проверяем, что типы структуры сохранились
        self.assertEqual(sorted_types, ['standard'] * 4)

    def test_sort_data_by_name_key_value(self):
        """Тест сортировки данных ключ-значение"""
        structure_types = ['key_value'] * 4
        sorted_data, sorted_types = sort_data_by_name(self.key_value_data, structure_types)

        # Проверяем порядок сортировки по ключам
        keys = [list(item.keys())[0] for item in sorted_data]
        self.assertEqual(keys, ['a_key', 'b_key', 'm_key', 'z_key'])

        # Проверяем, что типы структуры сохранились
        self.assertEqual(sorted_types, ['key_value'] * 4)

    def test_process_duplicates_with_sorting(self):
        """Тест обработки с сортировкой"""
        structure_types = ['standard'] * 4
        result, report = process_duplicates(self.standard_data, structure_types)

        # Проверяем, что результат отсортирован
        names = [item['name'] for item in result]
        self.assertEqual(names, sorted(names))

        # Проверяем содержимое
        self.assertEqual(len(result), 3)  # Один дубликат удален
        self.assertEqual(len(report), 1)  # Один объект в отчете

if __name__ == '__main__':
    unittest.main()