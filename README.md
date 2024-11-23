#  Работа №2
## *О чем работа?*
Необходимо составить программу - визуализатор зависимостей ***пакета Python***.  
Для графического представления используется ***PlantUML***.

Практическая работа содержит следующие функции:
- `parse_json_config` - разбирает конфигурационный xml и сохраняет настройки из него.
- `get_dependencies` - обращается к pip и получает зависимости запрошенного пакета.
- `get_git_commits` - получает список коммитов локального репозитория запрошенного пакета.
- `build_dependency_graph` - форматирует зависимости в формат `"A" --> B`.
- `generate_plantuml_script` - форматирует список зависимостей в формат PlantUML скрипта.
- `generate_plantuml_script_for_git` - форматирует список  коммитов в формат PlantUML скрипта.
- `save_plantuml_script` - сохраняет plantUML срипт в отдельный файл.
- `visualize_graph` - передаёт скрипт в утилиту plantUML.jar и визуализирует скрипт.

*Все* функции покрыты тестами.

## **Вывод:**
В результатах выполненной работы была написана программа визуализирующая зависимости пакетов Python.  
Все функции покрыты тестами.