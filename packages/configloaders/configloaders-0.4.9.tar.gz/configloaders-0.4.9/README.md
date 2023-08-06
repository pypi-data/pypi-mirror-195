Load configurations from a variety of configuration files and use them easily

# Examples

## Load configuration file if it exists

```python
import configloaders

username = 'username'
password = 'password'
phone = 123456789
auto_login = True

configloaders.load_json(globals())
```

## Load the configuration and update it on exit

```python
import configloaders

username = 'username'
password = 'password'
phone = 123456789
auto_login = True

configloaders.load_json(globals(), save_on_exit=True)
```

## Load the configuration and require the configuration file to exist

```python
import configloaders

username = 'username'
password = 'password'
phone = 123456789
auto_login = True

configloaders.load_json(globals(), required=True)
```

## Manually save the configuration

```python
import configloaders

username = 'username'
password = 'password'
phone = 123456789
auto_login = True

configloaders.load_json(globals()).dump()
configloaders.load_json(globals()).dump(original=True)
configloaders.dump()
configloaders.dump(original=True)
```

## Take all configuration items as command line arguments

```python
import configloaders

username = 'username'
password = 'password'
phone = 123456789
auto_login = True

configloaders.load_argparse(globals())
# or
import argparse
parser = argparse.ArgumentParser()
configloaders.load_argparse(globals(), parser)
parser.parse_args()
```

# Features

* Variables of the module type and those prefixed with "__" are ignored