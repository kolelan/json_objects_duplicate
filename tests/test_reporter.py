import unittest
import os
import json
from unittest.mock import mock_open, patch
from core.reporter import generate_report, save_result
from config.settings import DEFAULT_REPORT_FILE, DEFAULT_OUTPUT_FILE


class TestReporter(unittest.TestCase):

    def setUp(self):
        # Тестовые данные
        self.test_report_data = [
            {
                'line': 7,
                'name': 'ConfigController::actionSaveLastProject',
                'desc': 'Сохранение идентификатора последнего выгруженного проекта',
                'object': {'name': 'test', 'desc': 'test'}
            }
        ]

        self.test_result_data = [
            {'name': 'test1', 'desc': 'описание 1'},
            {'name': 'test2', 'desc': 'description 2'}
        ]

        # Очищаем тестовые файлы перед каждым тестом
        if os.path.exists('test_report.txt'):
            os.remove('test_report.txt')
        if os.path.exists('test_output.json'):
            os.remove('test_output.json')

    def tearDown(self):
        # Очищаем тестовые файлы после каждого теста
        if os.path.exists('test_report.txt'):
            os.remove('test_report.txt')
        if os.path.exists('test_output.json'):
            os.remove('test_output.json')

    def test_save_result_compact_format(self):
        """Тест сохранения в компактном формате"""
        save_result(self.test_result_data, 'test_output.json')

        # Проверяем, что файл создался
        self.assertTrue(os.path.exists('test_output.json'))

        # Проверяем содержимое файла (компактный формат)
        with open('test_output.json', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Должно быть 4 строки: [, объект1, объект2, ]
        self.assertEqual(len(lines), 4)

        # Проверяем формат
        self.assertEqual(lines[0].strip(), '[')
        self.assertTrue(lines[1].strip().startswith('{'))
        self.assertTrue(lines[1].strip().endswith(','))
        self.assertTrue(lines[2].strip().startswith('{'))
        self.assertEqual(lines[3].strip(), ']')

        # Проверяем, что JSON валиден
        with open('test_output.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
        self.assertEqual(content, self.test_result_data)


if __name__ == '__main__':
    unittest.main()