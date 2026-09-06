# Pydantic Extra Types

[![CI](https://github.com/pydantic/pydantic-extra-types/actions/workflows/ci.yml/badge.svg)](https://github.com/pydantic/pydantic-extra-types/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/pydantic/pydantic-extra-types/branch/main/graph/badge.svg)](https://codecov.io/gh/pydantic/pydantic-extra-types)
[![pypi](https://img.shields.io/pypi/v/pydantic-extra-types.svg)](https://pypi.python.org/pypi/pydantic-extra-types)
[![license](https://img.shields.io/github/license/pydantic/pydantic-extra-types.svg)](https://github.com/pydantic/pydantic-extra-types/blob/main/LICENSE)

A place for pydantic types that probably shouldn't exist in the main pydantic lib.

See [pydantic/pydantic#5012](https://github.com/pydantic/pydantic/issues/5012) for more info.

## Installation

Install this library with the desired extras dependencies as listed in [project.optional-dependencies](./pyproject.toml).

For example, if pendulum support was desired:

```shell
# via uv
$ uv add "pydantic-extra-types[pendulum]"

# via pip
$ pip install -U "pydantic-extra-types[pendulum]"
```

For phone numbers, choose `pydantic-extra-types[phonenumbers]` or
`pydantic-extra-types[phonenumberslite]`. Both support `PhoneNumber` and
`PhoneNumberValidator`. The lite distribution omits geocoder, carrier, and
timezone data that these types do not use. Install only one phone distribution:
they provide the same `phonenumbers` import namespace. The `all` extra continues
to include the full distribution.
