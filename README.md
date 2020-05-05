[![codecov](https://codecov.io/gh/devalv/utils/branch/master/graph/badge.svg)](https://codecov.io/gh/devalv/utils)

#### Создание env
pipenv install --dev

#### Активация env
pipenv shell

#### Запуск тестов
python -m unittest discover tests/

#### Запуск coverage и создание отчета
python3 -m coverage run -m unittest discover tests/ && python3 -m coverage html

#### Активация codecov
https://github.com/codecov/example-python