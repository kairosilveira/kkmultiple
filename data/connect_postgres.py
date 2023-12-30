import psycopg2
from dotenv import load_dotenv
import os
import polars as pl
import pandas as pd

load_dotenv()


class PostgresManager:
    def __init__(self) -> None:
        """
        Initialize a PostgresConnector instance.

        The constructor sets up the URL for connecting to the PostgreSQL database.

        """
        self.url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        self.connection = None
        self.cursor = None

    def _connect_to_postgres(self):
        """
        Establish a connection to the PostgreSQL database.

        This private method is responsible for creating a connection and cursor
        to interact with the database.

        """
        try:
            self.connection = psycopg2.connect(self.url)
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e

    def _close_connection(self):
        """
        Close the connection to the PostgreSQL database.

        This private method is responsible for closing the cursor and connection.

        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_table(self, table_name:str, columns_and_types:dict={}):
        """
        Create a new table in the PostgreSQL database.

        Parameters:
        - table_name (str): The name of the table to be created.
        - columns_and_types (dict): A dictionary specifying the columns and their data types.

        Example:
        {
            'id': 'serial',          # Serial is a shorthand for primary key
            'name': 'text',
            'age': 'int',
            'height': 'numeric(5,2)',
            'is_active': 'boolean',
            'created_at': 'timestamp',
            'data': 'jsonb',
            'tags': 'text[]',
            'status': 'enum("active", "inactive")'
        }

        Possible data types for columns:
        - Numeric Types: int, bigint, numeric(precision, scale)
        - Character Types: text, varchar(n)
        - Date/Time Types: date, time, timestamp
        - Boolean Type: boolean
        - Binary Data Types: bytea
        - JSON Types: json, jsonb
        - UUID Type: uuid
        - Array Type: integer[], text[], etc.
        - Other Types: hstore, tsvector
        """

        self._connect_to_postgres()
        column_definitions = ", ".join(
            [f"{column} {data_type}" for column, data_type in columns_and_types.items()])
        create_table_query = f'''
        CREATE TABLE {table_name} (
            {column_definitions}
        );
        '''
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    def insert_data(self, table_name:str, data_to_insert:dict):
        """
        Insert data into an existing table in the PostgreSQL database.

        Parameters:
        - table_name (str): The name of the table to insert data into.
        - data_to_insert (dict): A dictionary representing the data to be inserted.

        Example:
        {
        'name': 'John Doe little',
        'age': 30
        }
        """

        self._connect_to_postgres()
        insert_query = f'''
            INSERT INTO {table_name} ({", ".join(data_to_insert.keys())})
            VALUES ({", ".join([f"'{data}'" if isinstance(data, str) else str(data) for data in data_to_insert.values()])})
            '''
        try:
            self.cursor.execute(insert_query, tuple(data_to_insert.values()))
            self.connection.commit()
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    def get_table_data(self, table_name:str):
        """
        Retrieve information about tables and columns in the PostgreSQL database.

        Returns:
        - pl.DataFrame: A Polars DataFrame containing information about tables and columns.

        """
        self._connect_to_postgres()
        select_query = f'SELECT * FROM {table_name};'
        try:
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            # created as pd.DataFrame to fix the problem with big strings.
            df = pd.DataFrame(rows)
            df.columns = column_names
            return pl.DataFrame(df)

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    def get_tables_info(self):
        """
        Retrieve information about tables and columns in the PostgreSQL database.

        Returns:
        - pl.DataFrame: A Polars DataFrame containing information about tables and columns.

        """
        self._connect_to_postgres()
        tables_query = '''
            SELECT
                t.table_name,
                c.column_name
            FROM
                information_schema.tables t
            JOIN
                information_schema.columns c ON t.table_name = c.table_name
            WHERE
                t.table_schema = 'public';
            '''

        try:
            self.cursor.execute(tables_query)
            table_names = self.cursor.fetchall()
            df = pd.DataFrame(table_names, columns=['Table Name','Columns'])
            return pl.DataFrame(df)\
                .group_by('Table Name').agg(pl.col('Columns'))
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    def drop_table(self, table_name:str):
        """
        Drop an existing table in the PostgreSQL database.

        Parameters:
        - table_name (str): The name of the table to be dropped.

        """
        self._connect_to_postgres()
        drop_table_query = f'DROP TABLE IF EXISTS {table_name} RESTRICT;'
        try:
            self.cursor.execute(drop_table_query)
            self.connection.commit()
        except Exception as e:
            raise e
        finally:
            self._close_connection()
