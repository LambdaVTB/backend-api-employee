from service.configs.fastapi import FastapiSettings
from service.configs.postgres import PostgresSettings
from service.configs.neo4j import Neo4jSettings


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()


def get_fastapi_settings() -> FastapiSettings:
    return FastapiSettings()


def get_neo4j_settings() -> Neo4jSettings:
    return Neo4jSettings()
