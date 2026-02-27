"""Tests for DSN types migrated from pydantic.networks."""

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.dsn import (
    AmqpDsn,
    ClickHouseDsn,
    CockroachDsn,
    KafkaDsn,
    MariaDBDsn,
    MongoDsn,
    MySQLDsn,
    NatsDsn,
    PostgresDsn,
    RedisDsn,
    SnowflakeDsn,
)

# --- PostgresDsn ---


class PostgresModel(BaseModel):
    db: PostgresDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'postgresql://user:pass@localhost:5432/mydb',
        'postgresql://user:pass@localhost/mydb',
        'postgres://user:pass@localhost:5432/mydb',
        'postgresql+asyncpg://user:pass@localhost:5432/mydb',
        'postgresql+psycopg2://user:pass@localhost/mydb',
        'postgresql://user:pass@host1:5432,host2:5432/mydb',
    ],
)
def test_postgres_dsn_valid(dsn: str) -> None:
    m = PostgresModel(db=dsn)
    assert str(m.db) == dsn


@pytest.mark.parametrize(
    'dsn',
    [
        'http://localhost:5432/mydb',
        'mysql://user:pass@localhost/mydb',
    ],
)
def test_postgres_dsn_invalid_scheme(dsn: str) -> None:
    with pytest.raises(ValidationError):
        PostgresModel(db=dsn)


def test_postgres_dsn_host_required() -> None:
    with pytest.raises(ValidationError):
        PostgresModel(db='postgresql:///mydb')


# --- CockroachDsn ---


class CockroachModel(BaseModel):
    db: CockroachDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'cockroachdb://user:pass@localhost:26257/defaultdb',
        'cockroachdb+psycopg2://user:pass@localhost:26257/mydb',
        'cockroachdb+asyncpg://user:pass@localhost/mydb',
    ],
)
def test_cockroach_dsn_valid(dsn: str) -> None:
    m = CockroachModel(db=dsn)
    assert str(m.db) == dsn


def test_cockroach_dsn_host_required() -> None:
    with pytest.raises(ValidationError):
        CockroachModel(db='cockroachdb:///mydb')


# --- AmqpDsn ---


class AmqpModel(BaseModel):
    broker: AmqpDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'amqp://guest:guest@localhost:5672/',
        'amqps://user:pass@rabbit.example.com:5671/',
        'amqp://localhost',
    ],
)
def test_amqp_dsn_valid(dsn: str) -> None:
    m = AmqpModel(broker=dsn)
    assert str(m.broker) == dsn


def test_amqp_dsn_invalid_scheme() -> None:
    with pytest.raises(ValidationError):
        AmqpModel(broker='http://localhost:5672/')


# --- RedisDsn ---


class RedisModel(BaseModel):
    cache: RedisDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'redis://localhost:6379/0',
        'redis://:password@localhost:6379/1',
        'rediss://user:pass@redis.example.com:6380/0',
    ],
)
def test_redis_dsn_valid(dsn: str) -> None:
    m = RedisModel(cache=dsn)
    assert str(m.cache) == dsn


def test_redis_dsn_invalid_scheme() -> None:
    with pytest.raises(ValidationError):
        RedisModel(cache='http://localhost:6379/0')


# --- MongoDsn ---


class MongoModel(BaseModel):
    db: MongoDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'mongodb://user:pass@localhost:27017/mydb',
        'mongodb://localhost:27017',
        'mongodb+srv://user:pass@cluster.example.com:27017/mydb',
        'mongodb://host1:27017,host2:27017/mydb',
    ],
)
def test_mongo_dsn_valid(dsn: str) -> None:
    m = MongoModel(db=dsn)
    assert str(m.db) == dsn


def test_mongo_dsn_invalid_scheme() -> None:
    with pytest.raises(ValidationError):
        MongoModel(db='http://localhost:27017/mydb')


# --- KafkaDsn ---


class KafkaModel(BaseModel):
    broker: KafkaDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'kafka://localhost:9092',
        'kafka://broker1:9092',
    ],
)
def test_kafka_dsn_valid(dsn: str) -> None:
    m = KafkaModel(broker=dsn)
    assert str(m.broker) == dsn


# --- NatsDsn ---


class NatsModel(BaseModel):
    broker: NatsDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'nats://localhost:4222',
        'nats://user:pass@host1:4222,host2:4222',
        'tls://localhost:4222',
    ],
)
def test_nats_dsn_valid(dsn: str) -> None:
    m = NatsModel(broker=dsn)
    assert str(m.broker) == dsn


# --- MySQLDsn ---


class MySQLModel(BaseModel):
    db: MySQLDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'mysql://user:pass@localhost:3306/mydb',
        'mysql+pymysql://user:pass@localhost:3306/mydb',
        'mysql+asyncmy://user:pass@localhost:3306/mydb',
        'mysql+aiomysql://user:pass@localhost:3306/mydb',
    ],
)
def test_mysql_dsn_valid(dsn: str) -> None:
    m = MySQLModel(db=dsn)
    assert str(m.db) == dsn


def test_mysql_dsn_host_required() -> None:
    with pytest.raises(ValidationError):
        MySQLModel(db='mysql:///mydb')


# --- MariaDBDsn ---


class MariaDBModel(BaseModel):
    db: MariaDBDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'mariadb://user:pass@localhost:3306/mydb',
        'mariadb+pymysql://user:pass@localhost:3306/mydb',
        'mariadb+mariadbconnector://user:pass@localhost:3306/mydb',
    ],
)
def test_mariadb_dsn_valid(dsn: str) -> None:
    m = MariaDBModel(db=dsn)
    assert str(m.db) == dsn


def test_mariadb_dsn_host_required() -> None:
    with pytest.raises(ValidationError):
        MariaDBModel(db='mariadb:///mydb')


# --- ClickHouseDsn ---


class ClickHouseModel(BaseModel):
    db: ClickHouseDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'clickhouse://user:pass@localhost:8123/mydb',
        'clickhouses://user:pass@ch.example.com:8443/mydb',
        'clickhouse+native://user:pass@localhost:9000/mydb',
        'clickhouse+asynch://user:pass@localhost:8123/mydb',
    ],
)
def test_clickhouse_dsn_valid(dsn: str) -> None:
    m = ClickHouseModel(db=dsn)
    assert str(m.db) == dsn


# --- SnowflakeDsn ---


class SnowflakeModel(BaseModel):
    db: SnowflakeDsn


@pytest.mark.parametrize(
    'dsn',
    [
        'snowflake://user:pass@account.snowflakecomputing.com/mydb',
        'snowflake://user:pass@account.snowflakecomputing.com:443/mydb',
    ],
)
def test_snowflake_dsn_valid(dsn: str) -> None:
    m = SnowflakeModel(db=dsn)
    assert str(m.db) == dsn


def test_snowflake_dsn_host_required() -> None:
    with pytest.raises(ValidationError):
        SnowflakeModel(db='snowflake:///mydb')


# --- Cross-type validation ---


def test_all_dsn_types_reject_invalid_schemes() -> None:
    """Ensure each DSN type rejects URLs with wrong schemes."""
    models_and_bad_dsns = [
        (PostgresModel, 'mysql://localhost/db'),
        (CockroachModel, 'postgres://localhost/db'),
        (AmqpModel, 'redis://localhost'),
        (RedisModel, 'amqp://localhost'),
        (MongoModel, 'postgres://localhost/db'),
        (KafkaModel, 'amqp://localhost'),
        (MySQLModel, 'postgres://localhost/db'),
        (MariaDBModel, 'mysql://localhost/db'),
        (ClickHouseModel, 'postgres://localhost/db'),
        (SnowflakeModel, 'postgres://localhost/db'),
    ]
    for model_cls, dsn in models_and_bad_dsns:
        with pytest.raises(ValidationError):
            field = next(iter(model_cls.model_fields))
            model_cls.model_validate({field: dsn})
