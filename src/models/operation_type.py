from enum import Enum


class OperationType(Enum):
    """
    Enum for the different types of CRUD operations.
    """
    CREATE = ("PluralView", "post")
    READ = ("SingleView", "get")
    UPDATE = ("SingleView", "put")
    DELETE = ("SingleView", "delete")
    READ_ALL = ("PluralView", "get")

