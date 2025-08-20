# Конфигурационные переменные
NAME_FIELD = "name"
DESC_FIELD = "desc"

# Настройки файлов
DEFAULT_OUTPUT_FILE = "output.json"
DEFAULT_REPORT_FILE = "report.txt"

# Регулярные выражения
CYRILLIC_PATTERN = r'^[\u0400-\u04FF\s\d\-–—,\.:;!?\(\)\[\]{}"\'«»]+$'
LATIN_PATTERN = r'^[a-zA-Z\s\d\-–—,\.:;!?\(\)\[\]{}"\'<>]+$'

# Настройки форматирования
COMPACT_JSON = True  # Компактный формат JSON