import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


connection_string = f"""
    host={os.getenv('DB_HOST')}
    dbname={os.getenv('DB_NAME')}
    user={os.getenv('DB_USER')}
    password={os.getenv('DB_PASSWORD')}
    port={os.getenv('DB_PORT')}
"""

def get_connection():
    try:
        conn = psycopg2.connect(connection_string)
        print('Connected!')
        return conn
    except Exception as e:
        print(f'Failed! {e}')
        return None
    
conn = get_connection()

def get_user_unsafe(user_id):
    with get_connection() as conn:
        conn.set_session(autocommit=True) # 
        with conn.cursor() as cur:
            query = f'SELECT * FROM users WHERE id={user_id}'
            print(f'Exec: {query}')
            cur.execute(query)
            try:
                cur.fetchall()
            except Exception as e:
                print('Query failed', e)
                return None
            
user_input = '1; DROP TABLE users;'

def get_user(user_id):
    with conn.cursor() as cur:
        query = "SELECT * FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        #print(cur.query())
        print('Safe result: ', result)
        return result
# print(get_user(user_input))

# print(get_user_unsafe(user_input))

# REGEX

def find_emails(domain_pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = "SELECT email FROM users WHERE email ~ %s"
            # anton@test.com
            # ben@test.com
            #! julia@test.com
            pattern = f"^[Aab].*@{domain_pattern}$"
            cur.execute(query, (pattern,))
            results = cur.fetchall()
            for row in results:
                print(row[0])
            return results

find_emails("test\\.com") # test!com, test@com
if conn:
    conn.close()
