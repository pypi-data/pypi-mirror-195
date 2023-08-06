from __future__ import annotations

from typing import Iterable
from pathlib import Path

import psycopg as pg

from ..client import Client
from ..queries import first_values


__all__ = [
    "migrate"
]


def migrate(client: Client, paths: Iterable[str | Path]):
    """
    Execute SQL scripts to setup/migrate the database.
    The included `base.sql` script is always executed first.
    User-defined scripts are run in the order they are given.
    A script is never run twice.
    Whether a script has already been run before is determined by filename.
    Thus `base.sql` cannot be used as filename for user-defined scripts.

    Example script:
        BEGIN;

        ALTER TABLE metrics
            ADD COLUMN train_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN train_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN train_loss FLOAT,
            ADD COLUMN train_top1 FLOAT,
            ADD COLUMN train_top5 FLOAT,
            ADD COLUMN val_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN val_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN val_loss FLOAT,
            ADD COLUMN val_top1 FLOAT,
            ADD COLUMN val_top5 FLOAT,
            ADD COLUMN test_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN test_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN test_loss FLOAT,
            ADD COLUMN test_top1 FLOAT,
            ADD COLUMN test_top5 FLOAT;

        END;

    Parameters:
        client: Client to connect to the database
        paths: Paths to SQL scripts; executed in the order that they are given
    """
    with client.connect() as conn:
        with conn.cursor() as cursor:
            # create the schema if it does not exist
            if client.schema is not None:
                schema = client.schema
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
                conn.commit()
                print("Schema:", schema)
            # try to get names of applied migration files
            try:
                applied_names = set(first_values(
                    cursor, "SELECT name FROM applied_migrations;"))
            except pg.ProgrammingError:
                applied_names = set()
                conn.rollback()
            # base schema file is stored in the same folder as this module
            base = Path(__file__).parent / "base.sql"
            # execute scripts if they have not yet been applied
            for path in (base,) + tuple(paths):
                path = Path(path)
                if str(path.name) in applied_names:
                    print("(OK)", path.name)
                else:
                    with open(path, encoding='UTF-8') as fp:
                        script = fp.read()
                    cursor.execute(script)
                    cursor.execute(
                        "INSERT INTO applied_migrations (name) VALUES (%s)",
                        (str(path.name),),
                    )
                    print("(NEW)", path.name)
