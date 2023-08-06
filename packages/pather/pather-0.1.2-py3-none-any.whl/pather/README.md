# Pather

Parameters:

-   _string_ - string ("1", "author")

Returned OS path:

-   _string_ - directories (e.g., `a/1/e/4/`)

## Installation

```sh
pip install pather
```

## Usage

Pather by query:

```python
>>> import pather
>>> path = pather("string")
>>> path
'c/3/f/e/'
```

## Development setup

```sh
$ python3 -m venv env
$ . env/bin/activate
$ make deps
$ tox
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Make sure to add or update tests as appropriate.

Use [Black](https://black.readthedocs.io/en/stable/) for code formatting and [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/) for commit messages.

## [Changelog](CHANGELOG.md)

## License

[MIT](https://choosealicense.com/licenses/mit/)
