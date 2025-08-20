import unittest
from core.validator import is_cyrillic, is_latin, detect_object_structure, normalize_object


class TestValidator(unittest.TestCase):

    def test_is_cyrillic(self):
        self.assertTrue(is_cyrillic("Привет мир"))
        self.assertTrue(is_cyrillic("Сохранение файла 123"))
        self.assertTrue(is_cyrillic("Тест, с пунктуацией!"))
        self.assertFalse(is_cyrillic("Hello world"))
        self.assertFalse(is_cyrillic(""))
        self.assertFalse(is_cyrillic(None))

    def test_is_latin(self):
        self.assertTrue(is_latin("Hello world"))
        self.assertTrue(is_latin("Test with numbers 123"))
        self.assertTrue(is_latin("Test, with punctuation!"))
        self.assertFalse(is_latin("Привет мир"))
        self.assertFalse(is_latin(""))
        self.assertFalse(is_latin(None))

    def test_detect_object_structure(self):
        # Стандартная структура
        std_obj = {"name": "test", "desc": "description"}
        self.assertEqual(detect_object_structure(std_obj), "standard")

        # Структура ключ-значение
        kv_obj = {"ConfigController::actionSaveConfig": "Сохранение файла"}
        self.assertEqual(detect_object_structure(kv_obj), "key_value")

        # Неизвестная структура
        unknown_obj = {"field1": "value1", "field2": "value2"}
        self.assertEqual(detect_object_structure(unknown_obj), "unknown")

    def test_normalize_object(self):
        # Стандартная структура
        std_obj = {"name": "test", "desc": "description"}
        normalized = normalize_object(std_obj, "standard")
        self.assertEqual(normalized, {"name": "test", "desc": "description"})

        # Структура ключ-значение
        kv_obj = {"ConfigController::actionSaveConfig": "Сохранение файла"}
        normalized = normalize_object(kv_obj, "key_value")
        self.assertEqual(normalized, {"name": "ConfigController::actionSaveConfig", "desc": "Сохранение файла"})

        # Неизвестная структура
        unknown_obj = {"field1": "value1", "field2": "value2"}
        normalized = normalize_object(unknown_obj, "unknown")
        self.assertEqual(normalized, {"name": "", "desc": ""})


if __name__ == '__main__':
    unittest.main()