[![codecov](https://codecov.io/gh/devalv/utils/branch/master/graph/badge.svg)](https://codecov.io/gh/devalv/utils)
![tests](https://github.com/devalv/utils/workflows/tests/badge.svg)
![build](https://github.com/devalv/utils/workflows/build/badge.svg)

# Set of tools that often have to reproduce in Python scripts.

## descriptors
Descriptors for extra type checking.

### descriptors.TypeChecker
Universal descriptor for type checking.
Then __set__ called - checks that attribute value type equals value_type.

#### Usage example:
```
class Foo:
    bar = TypeChecker('bar', list)

    def __init__(self, bar):
        self.bar = bar
```

### descriptors.StringType(TypeChecker)
Descriptor for string checking. Send __str__ as TypeChecker value_type.

#### Usage example:
```
class Foo:
    bar = StringType('bar')

    def __init__(self, bar):
        self.bar = bar
```

### descriptors.IntType(TypeChecker)
Descriptor for string checking. Send __int__ as TypeChecker value_type.

### descriptors.ListType(TypeChecker)
Descriptor for string checking. Send __list__ as TypeChecker value_type.

### descriptors.DictType(TypeChecker)
Descriptor for string checking. Send __dict__ as TypeChecker value_type.

### descriptors.WritableFile(StringType)
Descriptor for new file checking. Check that file (value) is a writable file or can be created.

### descriptors.HttpMethod(StringType)
Descriptor for http method checking. Check that value is one of http methods.

### Custom descriptor example
```
class HttpMethodType(StringType):
    http_methods = frozenset(['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'PATCH', 'OPTIONS'])

    def __set__(self, instance, value):
        super().__set__(instance, value)
        if value not in self.http_methods:
            instance.__dict__[self.name] = None
            raise TypeError(f'{self.name}={value} is not a HTTP Method.')
```

## logger

### logger.Logging
Script logger configuration and methods.
```
log_date_fmt: log date format (only str)
log_fmt: log format (only str)
log_lvl: log level (logging.DEBUG, logging.INFO and etc.)
file_handler is missing intentionally. Use OS features.
```

#### log DEBUG level message:
```
Logging().debug('message')
```

#### log INFO level message:
```
Logging().info('message')
```

#### log WARNING level message:
```
Logging().warning('message')
```

#### log ERROR level message:
```
Logging().error('message')
```

#### log CRITICAL level message:
```
Logging().critical('message')
```

## utils
Some utils for pure python scripts.
### utils.Util
Some useful utils methods.

#### Util().update(attrs_dict: dict)
Update class public attrs.

#### Util.check_exists(file_path: str)
Raises FileNotFoundError if file_path not exists.

#### Util.check_not_exists(file_path: str)
Raises FileExistsError if file_path already exists.

#### Util.check_extension(file_name: str, extension_list: frozenset)
Compare extension of file_name and extension.

```
file_name example: 'config.json'
extension_list example: ('.json')
```

#### Util.str_to_date(date_str: str, date_fmt: str)
Convert str to date.

#### Util.date_to_str(date: datetime.date, date_fmt: str)
Convert date/datetime to str.

#### Util.read_file_gen(file_name: str)
Generator object that line by line read the __file_name__ file.

#### Util.save_text_file(file_path: str, txt_data)
Save file in plaint text format.
txt_data can be List, Generator or String.

#### Util.save_json_file(file_path: str, json_data)
Save file in JSON format.

#### Util().public_attrs()
Return dictionary of class public attributes and properties (attrs that starts '_' 
and properties are excluded).

## config
Extendable config template.

### config.Config(Util)
Script configuration.
```
logging parameters:
    log_date_fmt: log date format (only str)
    log_fmt: log format (only str)
    log_lvl: log level (logging.DEBUG, logging.INFO and etc.)

__extensions: acceptable configuration file extensions
```

#### Config().log
Script logger instance.

##### debug message example
```
cfg = Config()
cfg.log.debug('test')
```

#### Config().load(config_file: str)
Load configuration attributes from a config_file.

#### Config().create_template(file_path: str)
Create JSON config file template.

#### Usage example
```
import argparse

from dav_utils.config import Config


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

## Running tests
python -m unittest discover tests/