"""
Storage file format definitions
"""

# TODO: Replace this with an enum

__author__ = 'Gareth Coles'

YAML = "Yaml"
JSON = "JSON"
MEMORY = "Memory"
DBAPI = "DBAPI"
MONGO = "MongoDB"
REDIS = "Redis"

DATA = [YAML, JSON, MEMORY, DBAPI, MONGO, REDIS]
CONF = [YAML, JSON, MEMORY]
ALL = [YAML, JSON, MEMORY]
