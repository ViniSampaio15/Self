import psycopg2
import psycopg2.extras


def get_tables(connection):

    """
    Create and return a list of dictionaries with the
    schemas and names of tables in the database
    connected to by the connection argument.
    """

    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    print(cursor.rowcount)
    cursor.execute("""SELECT table_schema, table_name
                      FROM information_schema.tables
                      WHERE table_schema != 'pg_catalog'
                      AND table_schema != 'information_schema'
                      AND table_type='BASE TABLE'
                      ORDER BY table_schema, table_name""")

    tables = cursor.fetchall()

    cursor.close()

    return tables


def print_tables(tables):

    """
    Prints the list created by get_tables
    """

    for row in tables:

        print("{}.{}".format(row["table_schema"], row["table_name"]))