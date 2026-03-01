"""DSN (Data Source Name) types for common databases and message brokers.

Migrated from `pydantic.networks` as part of pydantic#9071.
These types provide validated connection strings for various databases and services.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import UrlConstraints
from pydantic_core import MultiHostUrl, Url

__all__ = [
    'AmqpDsn',
    'ClickHouseDsn',
    'CockroachDsn',
    'KafkaDsn',
    'MariaDBDsn',
    'MongoDsn',
    'MySQLDsn',
    'NatsDsn',
    'PostgresDsn',
    'RedisDsn',
    'SnowflakeDsn',
]


# --- Single-host DSN types (based on Url) ---

CockroachDsn = Annotated[
    Url,
    UrlConstraints(
        host_required=True,
        allowed_schemes=[
            'cockroachdb',
            'cockroachdb+psycopg2',
            'cockroachdb+asyncpg',
        ],
    ),
]
"""A type that will accept any Cockroach DSN.

* Host required
* Supported schemes: `cockroachdb`, `cockroachdb+psycopg2`, `cockroachdb+asyncpg`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import CockroachDsn

class MyModel(BaseModel):
    db: CockroachDsn

m = MyModel(db='cockroachdb://user:pass@localhost:26257/defaultdb')
print(m.db)
#> cockroachdb://user:pass@localhost:26257/defaultdb
```
"""

AmqpDsn = Annotated[
    Url,
    UrlConstraints(allowed_schemes=['amqp', 'amqps']),
]
"""A type that will accept any AMQP DSN.

* Host not required
* Supported schemes: `amqp`, `amqps`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import AmqpDsn

class MyModel(BaseModel):
    broker: AmqpDsn

m = MyModel(broker='amqp://guest:guest@localhost:5672/')
print(m.broker)
#> amqp://guest:guest@localhost:5672/
```
"""

RedisDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=['redis', 'rediss'],
        default_host='localhost',
        default_port=6379,
        default_path='/0',
    ),
]
"""A type that will accept any Redis DSN.

* Host required (defaults to `localhost`)
* Default port: 6379
* Default path: `/0`
* Supported schemes: `redis`, `rediss`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import RedisDsn

class MyModel(BaseModel):
    cache: RedisDsn

m = MyModel(cache='redis://:password@localhost:6379/0')
print(m.cache)
#> redis://:password@localhost:6379/0
```
"""

KafkaDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=['kafka'],
        default_host='localhost',
        default_port=9092,
    ),
]
"""A type that will accept any Kafka DSN.

* Host not required (defaults to `localhost`)
* Default port: 9092
* Supported schemes: `kafka`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import KafkaDsn

class MyModel(BaseModel):
    broker: KafkaDsn

m = MyModel(broker='kafka://localhost:9092')
print(m.broker)
#> kafka://localhost:9092
```
"""

MySQLDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=[
            'mysql',
            'mysql+mysqlconnector',
            'mysql+aiomysql',
            'mysql+asyncmy',
            'mysql+mysqldb',
            'mysql+pymysql',
            'mysql+cymysql',
            'mysql+pyodbc',
        ],
        default_port=3306,
        host_required=True,
    ),
]
"""A type that will accept any MySQL DSN.

* Host required
* Default port: 3306
* Supported schemes: `mysql` and common driver variants

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import MySQLDsn

class MyModel(BaseModel):
    db: MySQLDsn

m = MyModel(db='mysql://user:pass@localhost:3306/mydb')
print(m.db)
#> mysql://user:pass@localhost:3306/mydb
```
"""

MariaDBDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=[
            'mariadb',
            'mariadb+mariadbconnector',
            'mariadb+pymysql',
        ],
        default_port=3306,
        host_required=True,
    ),
]
"""A type that will accept any MariaDB DSN.

* Host required
* Default port: 3306
* Supported schemes: `mariadb` and common driver variants

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import MariaDBDsn

class MyModel(BaseModel):
    db: MariaDBDsn

m = MyModel(db='mariadb://user:pass@localhost:3306/mydb')
print(m.db)
#> mariadb://user:pass@localhost:3306/mydb
```
"""

ClickHouseDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=[
            'clickhouse',
            'clickhouses',
            'clickhouse+native',
            'clickhouse+asynch',
        ],
        default_host='localhost',
        default_port=8123,
    ),
]
"""A type that will accept any ClickHouse DSN.

* Host not required (defaults to `localhost`)
* Default port: 8123
* Supported schemes: `clickhouse`, `clickhouses`, `clickhouse+native`, `clickhouse+asynch`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import ClickHouseDsn

class MyModel(BaseModel):
    db: ClickHouseDsn

m = MyModel(db='clickhouse://user:pass@localhost:8123/mydb')
print(m.db)
#> clickhouse://user:pass@localhost:8123/mydb
```
"""

SnowflakeDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=['snowflake'],
        host_required=True,
    ),
]
"""A type that will accept any Snowflake DSN.

* Host required
* Supported schemes: `snowflake`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import SnowflakeDsn

class MyModel(BaseModel):
    db: SnowflakeDsn

m = MyModel(db='snowflake://user:pass@account.snowflakecomputing.com/mydb')
print(m.db)
#> snowflake://user:pass@account.snowflakecomputing.com/mydb
```
"""


# --- Multi-host DSN types (based on MultiHostUrl) ---

PostgresDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=True,
        allowed_schemes=[
            'postgres',
            'postgresql',
            'postgresql+asyncpg',
            'postgresql+pg8000',
            'postgresql+psycopg',
            'postgresql+psycopg2',
            'postgresql+psycopg2cffi',
            'postgresql+py-postgresql',
            'postgresql+pygresql',
        ],
    ),
]
"""A type that will accept any Postgres DSN.

* Host required
* Supports multiple hosts
* Supported schemes: `postgres`, `postgresql` and common driver variants

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import PostgresDsn

class MyModel(BaseModel):
    db: PostgresDsn

m = MyModel(db='postgresql://user:pass@localhost:5432/mydb')
print(m.db)
#> postgresql://user:pass@localhost:5432/mydb
```
"""

MongoDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        allowed_schemes=['mongodb', 'mongodb+srv'],
        default_port=27017,
    ),
]
"""A type that will accept any MongoDB DSN.

* User info not required
* Port not required (defaults to 27017)
* Supports multiple hosts
* Supported schemes: `mongodb`, `mongodb+srv`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import MongoDsn

class MyModel(BaseModel):
    db: MongoDsn

m = MyModel(db='mongodb://user:pass@localhost:27017/mydb')
print(m.db)
#> mongodb://user:pass@localhost:27017/mydb
```
"""

NatsDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        allowed_schemes=['nats', 'tls', 'ws'],
        default_host='localhost',
        default_port=4222,
    ),
]
"""A type that will accept any NATS DSN.

* Host not required (defaults to `localhost`)
* Default port: 4222
* Supports multiple hosts
* Supported schemes: `nats`, `tls`, `ws`

```python
from pydantic import BaseModel
from pydantic_extra_types.dsn import NatsDsn

class MyModel(BaseModel):
    broker: NatsDsn

m = MyModel(broker='nats://localhost:4222')
print(m.broker)
#> nats://localhost:4222
```
"""
