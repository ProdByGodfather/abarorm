"""
Abarorm Package Initialization

This file imports the necessary database models to be exposed publicly.
The following models are available:
    - SQLiteModel
    - PostgreSQLModel
"""

__all__ = [
    'SQLiteModel',
    'PostgreSQLModel'
]

try:
    from .sqlite import SQLiteModel
    from .psql import PostgreSQLModel
except ImportError as e:
    raise ImportError(f"Error importing module: {e}")