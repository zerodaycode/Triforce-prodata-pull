import logging
import psycopg2
from secrets import postgres

log = logging.getLogger(__name__)


class Database:

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    def open(self):
        try:
            # Connect to PostgreSQL server
            log.info(f'Connecting to the PostgreSQL database "{self.db_name}"')
            self.conn = psycopg2.connect(database=self.db_name,
                                         user=postgres['user'],
                                         password=postgres['password'],
                                         host=postgres['host'],
                                         port=postgres['port'])
            log.info(f'Connection successful')

        except (Exception, psycopg2.DatabaseError) as error:
            log.exception(f"Can't connect to database")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def set_database(self, db_name: str):
        self.db_name = db_name

    def get(self, table: str, columns: list = None, limit=None):
        if not columns:
            columns = "*"
        stmt = f"SELECT {columns} FROM {table};"

        if limit:
            stmt += f"LIMIT {limit}"
        result = self.query(stmt, None, True)

        return result

    def insert_row(self, table: str, columns: list, data_row: list):

        if columns and len(data_row) != len(columns):
            raise ValueError(f"Missmatch of columns({len(columns)}) and values {len(data_row)}")
        stmt = f"INSERT INTO {table} "
        if columns:
            columns_to_string = ", ".join(columns)
            stmt += f"({columns_to_string}) "
        stmt += f"VALUES ({', '.join(['%s ' for _ in data_row])});"

        self.query(stmt, data_row)

    def insert_rows(self, table: str, columns: list, data_rows: list):

        stmt = f"INSERT INTO {table} "
        if columns:
            for i, params_row in enumerate(data_rows):
                if len(params_row) != len(columns):
                    raise ValueError(f"Missmatch of columns({len(columns)}) and values {len(params_row)} "
                                     f"on element number {i} with values({params_row})")

            columns_to_string = ", ".join(columns)
            stmt += f"({columns_to_string}) "

        stmt += "VALUES " + ",".join([f"({', '.join(['%s ' for _ in row])})" for row in data_rows]) + ";"

        self.query(stmt, [param for params_row in data_rows for param in params_row])

    def query(self, stmt: str, params=None, fetch: bool = False):
        self.open()
        # log.info(f"Statement : {stmt}")
        with self.conn.cursor() as curs:
            curs.execute(stmt, params)
            if fetch:
                result = curs.fetchall()
        self.close()
        if fetch:
            return result
