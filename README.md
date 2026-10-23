# Лабораторная работа 2. Потоковый анализатор файлов

### Установка
pip install -e .

### Использование
python -m streamstats analyze INPUT --format csv|jsonl [--output REPORT.json] [--skip-invalid]

### Тестирование 
python -m pytest  
## Реализация:
* errors — Кастомные ошибки (исключения)
* models — Модель Event и её валидация.
* parsers — Парсеры CSV и JSONL.
* analysis — Накопление и подсчёт статистики.
* report — Сохранение отчёта в JSON.
* __main__ — CLI-интерфейс и запуск программы.