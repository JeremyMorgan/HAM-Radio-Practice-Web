import sqlite3

class DatabaseConnection:
    def __init__(self, db_path: str) -> None:
        """
        Initializes a new instance of the DatabaseConnection class with the specified database path.

        Parameters:
        - `db_path` (str): The path to the SQLite database file.

        This method sets the database path for the connection and does not return any value.
        """
        self.db_path = db_path

    def __enter__(self) -> sqlite3.Cursor:
        """
        Establishes a connection to the SQLite database specified by `db_path` and returns a cursor object.

        Parameters:
        - `db_path` (str): The path to the SQLite database file.

        Returns:
        - `sqlite3.Cursor`: A cursor object representing the connection to the database.

        This method is used in a context manager to ensure that the database connection is properly closed and committed after use.
        """
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection and commits any pending changes.

        Parameters:
        - `exc_type` (type): The exception type that was raised. This is typically `None` unless an exception was caught.
        - `exc_val` (base exception class): The exception value. This is typically `None` unless an exception was caught.
        - `exc_tb` (traceback object): The traceback object associated with the exception. This is typically `None` unless an exception was caught.

        This method is called when the context manager is exiting, ensuring that the database connection is properly closed and committed after use.
        """
        self.connection.commit()
        self.connection.close()
