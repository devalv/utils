[![codecov](https://codecov.io/gh/devalv/utils/branch/master/graph/badge.svg)](https://codecov.io/gh/devalv/utils)
![Python package](https://github.com/devalv/utils/workflows/Python%20package/badge.svg)

#### Creating env
pipenv install --dev

#### Activating env
pipenv shell

#### Running tests
python -m unittest discover tests/

#### Coverage run and creating html report
python3 -m coverage run -m unittest discover tests/ && python3 -m coverage html

#### Using codecov
https://github.com/codecov/example-python

#### Usage example
```
import argparse

from utils import Config


def parse_args():
    """Incoming script arguments parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json', type=str,
                        help='Path to configuration file, ex: config.json')
    parser.add_argument('--template', default=False, type=bool,
                        help='Create config template')
    return parser.parse_args()


def main():  # pragma: no cover
    """Strait execution examples."""
    args = parse_args()

    if args.template:
        cfg = Config()
        cfg.log.debug('Trying to create template of configuration file.')
        cfg.create_template(args.config)
        cfg.log.debug('Exit.')
        sys.exit(0)

    try:
        user_config = Config(args.config)
        user_config.log.debug(f'Configuration file loaded: {user_config.public_attrs()}')
    except (AssertionError, FileExistsError):
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
```