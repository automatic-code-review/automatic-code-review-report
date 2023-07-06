import psycopg2
import os


def connection():
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_port = os.environ.get('DB_PORT')
    db_password = os.environ.get('DB_PASSWORD')

    return psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password, port=db_port)


def migration():

    script_path = os.path.abspath(
        os.path.dirname(os.path.abspath(__file__)) + "/../resources/db/migration/V1__initial.sql")

    with open(script_path, 'r') as script_file:
        script = script_file.read()

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(script)
        conn.commit()
    except (Exception, psycopg2.DatabaseError):
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
