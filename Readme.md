# Использование:
Установка зависимостей:

```bash
pip install -r requirements.txt
```
Запуск тестов:

```bash
python -m unittest discover tests
```
Обработка стандартного JSON:

```bash
python main.py input.json
```
Обработка ключ-значение JSON:

```bash
python main.py key_value_input.json
``` 
Режим "оставлять первый":

```bash
python main.py input.json --keep-first
``` 
Проект имеет модульную структуру, поддерживает оба формата JSON и покрыт тестами.