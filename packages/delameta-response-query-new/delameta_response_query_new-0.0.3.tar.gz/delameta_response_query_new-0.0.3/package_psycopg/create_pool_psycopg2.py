from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import register_inet
from psycopg2.pool import ThreadedConnectionPool
import psycopg2
from contextlib import contextmanager
__all__ = [
    "create_connection_postgresql"
]


@contextmanager
def connection_psycopg(commit:bool = None, pg_db_name:str = None, pg_user:str = None, pg_password:str = None, pg_host:str = None, pg_port:str = None, connect_timeout:int = None):
    """Untuk membuka koneksi
    commit => commit
    pg_db_name => nama database
    pg_user => usernya
    pg_password => passswordnya
    pg_host => hostnya
    pg_port => portnya
    connect_timeout => default 10 detik
    
    """
    commit = False if not commit else True
    try:
        pool = ThreadedConnectionPool(1, 500,
            database=pg_db_name,
            user=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            connect_timeout= int(connect_timeout) if connect_timeout else 10)
        
        @contextmanager
        def get_db_connection_lattol():
            try:
                connection = pool.getconn()
                yield connection
            finally:
                pool.putconn()
        with get_db_connection_lattol() as connection:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()
    except Exception as e:
        response = {'status':'error','message':"Offline "+str(e)}
    return response

create_connection_postgresql = connection_psycopg