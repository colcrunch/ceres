import os

from mysql import connector
from dotenv import load_dotenv

from .loggers import get_logger

if os.path.exists("../.env.dev"):
    load_dotenv("../.env.dev")
else:
    load_dotenv("../.env")

logger = get_logger(__name__)


class DBConn:
    """
    Provides contextual access to the mysql connector.
    """
    def __init__(self):
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASS", "")
        db_name = os.getenv("DB_NAME", "")
        db_host = os.getenv("DB_HOST", "localhost")

        self.connection_info = {
            "user": user,
            "password": password,
            "host": db_host,
            "database": db_name
        }

    def __enter__(self):
        self.con = connector.connect(**self.connection_info)
        yield self.con

    def __exit__(self):
        self.con.close()


class DBCursor:
    """
    Provides contextual access to a mysql cursor.
    Requires a connection to be passed during initialization.
    """
    def __init__(self, connection: connector.MySQLConnection):
        self.con = connection

    def __enter__(self):
        self.cursor = self.con.cursor()
        yield self.cursor

    def __exit__(self):
        try:
            # Try to commit the changes
            self.con.commit()
        except Exception as e:
            # If for what ever reason we are unable to commit the changes, roll them back.
            logger.warning(f"Error committing changes to database. {e}")
            logger.warning(e.__traceback__)
            self.con.rollback()
        finally:
            self.cursor.close()
