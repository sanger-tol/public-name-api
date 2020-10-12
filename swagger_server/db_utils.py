import sqlite3
import json
import pandas as pd

from swagger_server.file_utils import read_tsv


def get_db_cols_and_file_name(table_name=None):
    db_cols_public_names = ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    db_cols_unique_ids = ['public_name', 'species', 'specimen_id', 'pub_number', 'ignore']

    if table_name == 'public_names':
        return db_cols_public_names, 'final_merged.txt'
    return db_cols_unique_ids, 'unique_ids_assigned.txt'

def get_db(conn=None):
    if not conn:
        try:
            conn = sqlite3.connect("public_names.db")
        except Exception as e:
            print('Cound not find database file public_names.db. Error: ' + str(e))
    cur = conn.cursor()
    return conn, cur

def populate_db():
    created = False
    conn, cur = get_db(conn=None)
    try:
        with conn:
            for table_name in ['public_names', 'unique_ids']:
                try:
                    print("drop table " + table_name + ";")
                    cur.execute("drop table " + table_name + ";")
                except Exception as e:
                    print("Could not drop the " + table_name + " table. Ignore this error if the database is new. Error: " + str(e))

            cur.execute('create table public_names(prefix varchar, species varchar, taxid int, common_name varchar, genus varchar, family varchar, tax_order varchar, class varchar, phylum varchar);')
            cur.execute('create table unique_ids(public_name varchar, species varchar, specimen_id varchar, pub_number varchar, ignore varchar);')

    except Exception as e:
        print('Database creation failed. Error: ' + str(e))
        # return created

    df = None
    row_count = 0
    for table_name in ['public_names', 'unique_ids']:
        db_cols, tsv_file_name = get_db_cols_and_file_name(table_name=table_name)
        try:
            df = read_tsv(file_name=tsv_file_name)
            row_count = df.shape[0]  # number of rows
            # col_count = df.shape[1]  # number of columns
        except Exception as e:
            print('Could not read the public name tsv file {tsv_file_name}. Error: ' + str(e))
            return created, row_count, conn    
            
        try:
            # Add to the database
            df.columns = db_cols  # There are no column names in the tsv file, so need to add
            df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
            conn.commit()  # Should not have to, but just in case
        except Exception as e:
            print('Could not add the public names to the local database. Error: ' + str(e))
            return created 

    return True, row_count, conn

def query_local_database(conn=None, cur=None, tax_id=None, specimen_id=None, print_all=False):
    """
    Query rows in the public_name table
    :param conn: the Connection object
    :param cur: the Cursor object
    :param tax_id: the Taxon id to search for
    :param print_all: print results to screen
    :return:
    """
    if not conn:
        conn, cur = get_db(conn=None)

    if not cur:    
        cur = conn.cursor()

    # public_names = ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    # unique_ids = ['public_name', 'species', 'specimen_id', 'pub_number']
    if tax_id and specimen_id:
        cur.execute("SELECT a.prefix, b.public_name, a.species, a.taxid, a.common_name, a.genus, a.family, a.tax_order, a.class, a.phylum, b.specimen_id FROM public_names a, unique_ids b where a.species = b.species AND a.taxid=? and b.specimen_id=?", (tax_id,specimen_id))

    rows = cur.fetchall()

    if print_all:
        for row in rows:
            print(row)
    return rows

def update_local_database(conn=None, cur=None, query_str=None, tax_id=None, specimen_id=None, print_all=False):
    """
    Query rows in the public_name table
    :param conn: the Connection object
    :param cur: the Cursor object
    :param query_str: the Taxon id to search for
    :param print_all: print results to screen
    :return:
    """
    if not conn:
        conn, cur = get_db(conn=None)

    if not cur:    
        cur = conn.cursor()



    if query_str:
        cur.execute("SELECT * FROM public_names LEFT JOIN where taxid=?", (query_str,))  # ToDo, join with the unique_ids table

    rows = cur.fetchall()

    if print_all:
        for row in rows:
            print(row)
    return rows