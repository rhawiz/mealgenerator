# -*- coding: utf-8 -*-


import sqlite3
from time import sleep
from requests import ConnectionError

from utils import csv_to_list, to_ascii, print_progress
import os


def insert_row(db_path, table_name, row):
    connection = sqlite3.connect(db_path)
    connection.text_factory = str
    cursor = connection.cursor()
    value_placeholders = ''
    values = []
    for i in row:
        try:
            content = str(i)
        except UnicodeEncodeError:
            content = i.encode("utf-8")
        values.append(content)
        value_placeholders = "{}?, ".format(value_placeholders)

    value_placeholders = value_placeholders[:-2]

    insert_sql = 'INSERT INTO {} VALUES ({})'.format(table_name, value_placeholders)
    cursor.execute(insert_sql, tuple(values))
    connection.commit()
    connection.close()


def create_database(db_path, table_name, columns):
    """
    Create sqlite database and tables
    Parameters
    ----------
    db_path: str
        Database path
    table_name: str
        Table name
    columns: list<str>
        Column names

    Returns
    -------

    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    columns_sql = ''
    for column in columns:
        columns_sql = "{}{} TEXT, ".format(columns_sql, column)
    columns_sql = "({})".format(columns_sql[:-2])
    create_table_sql = '''CREATE TABLE {} {}'''.format(table_name, columns_sql)

    try:
        cursor.execute(create_table_sql)
        connection.commit()
        return True
    except sqlite3.OperationalError, e:
        print e
        # If the table exists check if the columns matches with the input columns
        #   if they are the same return True. If they don't match return False.
        cursor = connection.execute('SELECT * FROM {}'.format(table_name))
        existing_columns_hash = hash(''.join([description[0] for description in cursor.description]))
        columns_hash = hash(''.join(columns))
        if columns_hash == existing_columns_hash:
            return True
        return False
    finally:
        connection.close()


def execute_query(db_path, sql_query, columns=True):
    """
    Execute sql query on a sqlite database

    Parameters
    ----------
    db_path: str
        file path to sqlite database

    sql_query: str
        query to execute

    Returns
    -------
        bool/list<tuple>/none depending on the query

    """
    connection = sqlite3.connect(db_path)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute(sql_query)
    connection.commit()
    data = cursor.fetchall()

    if columns:
        data_columns = tuple(map(lambda x: x[0], cursor.description))
    connection.close()
    return [data_columns] + data


def csv_to_sqlite(csv_path, headers=None, db_path=None, table_name=None, process_row_function=None):
    """
    Converts csv into a sqlite database. If no headers passed, will name columns
    Parameters
    ----------
    csv_path: str
        CSV file path
    headers: tuple
        Tuple containing headers. len must be the same as as csv path or output of process_func
    db_path:
        SQLite database name. If none, will use the name of the CSV file as the filename. Defaults to None.
    process_row_function: function
        Call function on each row prior to conversion


    Returns
    -------
    bool
        True if database successfully created, False if failed.

    """

    if not os.path.exists(csv_path):
        print "File {} does not exist.".format(csv_path)
        return False

    csv_path = csv_path.replace("\\", "/")

    if not db_path:
        db_path = "{}.sqlite".format(csv_path.split("/")[-1].split(".")[0])

    if not table_name:
        table_name = db_path.split(".")[0]

    print "Loading data from {}".format(csv_path)

    data = csv_to_list(csv_path, has_headers=False)

    first_row = data.pop(0)

    count = len(data)

    print "\tfound {} rows.".format(count)

    if headers == None:
        headers = tuple([to_ascii(header) for header in first_row])

    print "Creating/loading database"
    status = create_database(db_path, table_name, headers)
    print "\tsuccess" if status else "\tfailed"
    if not status:
        return

    progress = 0
    success_count = 0
    fail_count = 0
    print "Populating database"
    for row in data:
        progress += 1
        print_progress(progress, count)
        if process_row_function:
            row = process_row_function(row)
            try:
                insert_row(db_path, table_name, row)
                success_count += 1
            except Exception:
                fail_count += 1
    print "Complete {} rows successfully inserted and {} failures.".format(success_count, fail_count)


if __name__ == "__main__":
    data = execute_query("../data/us_uk_nl_addresses.sqlite",
                         "SELECT address, HTML from addresses where country = 'NL'")
    print len(data)
    # csv_to_sqlite(
    #     "../data/uk_nl_addresses.csv",
    #     headers=("address", "type", "url", "country", "source", "html"),
    #     table_name="addresses",
    #     process_row_function=get_html
    # )
