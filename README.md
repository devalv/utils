#### Создание env
pipenv install --dev

#### Активация env
pipenv shell

#### Запуск тестов
python -m unittest discover tests/

#### Запуск coverage и создание отчета
python3 -m coverage run -m unittest discover tests/ && python3 -m coverage html
