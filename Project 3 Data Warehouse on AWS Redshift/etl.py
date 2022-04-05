import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Read the information from our S3 repository in the schema tables of the sql_queries script
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Gets and inserts the data from the staging tables into the dimensional tables of our schema using the queries declared on the sql_queries script
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Load the data from our S3, transform the metadata and insert it into the dimensions of our schema
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()