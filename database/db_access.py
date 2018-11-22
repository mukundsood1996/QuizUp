"""
This file contains the code that connects the backend to database
Run this file to check if the connection to database works
If it doesn't throw an error, it works!

postgres configuration - \conninfo
Connect from cmd: psql -h localhost -p 5432 -U postgres quizup
"""

import logging
import re
import string
from random import choice

import psycopg2

none_list = ['None', None, False, {}, [], set(), 'null', 'NULL', 0, "0", tuple(), (None,)]

def random_alnum(prefix: str = "", length: int = 4) -> str:
    """
    Generates a random alphanumeric of given length with a prefix
    :param prefix: string to be prepended to the alphanumeric
    :param length: length of the random alphanumeric
    :return: a string of the alphanumeric
    """
    x = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    return prefix + x

def _execute_query(query: str, json_output: bool = False, data=None) -> any:
    """
    Helper function to execute any query and fetches all rows
    :param query: Query string in SQL
    :param json_output: True when return type is expected to be of JSON format
    :return: None if query unsuccessful,
                list of tuples for SELECT query
                number of rows updated for UPDATE query
                number of rows inserted for INSERT query
    """
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            if json_output:
                json_query = """SELECT array_to_json(array_agg(row_to_json(t))) FROM ({}) t"""
                query = json_query.format(query)
            if data:
                cur.execute(query, data)
            else:
                cur.execute(query)
            logging.info('Executed: ' + query)
            res = cur.rowcount
            if re.fullmatch(r"^SELECT.*", query, re.IGNORECASE):
                if json_output:
                    res = cur.fetchone()
                else:
                    res = cur.fetchall()
            logging.info('Returned: ' + str(res))
            conn.commit()
            cur.close()
            return res

        except psycopg2.ProgrammingError as e:
            logging.error('Something went wrong with the query: %s', e)
            return None

        except psycopg2.IntegrityError as e:
            logging.error('Something went wrong with the query: %s', e)
            return None

        except psycopg2.OperationalError as e:
            logging.error('Operational error: %s', e)
            return None
    return None

def connect_db():
    """
    Connects to the postgres database
    :return: postgres connection object
    """
    connect_str = "dbname='quizup' user='postgres' host='localhost' password='welcomeback' port='5432'"
    try:
        conn = psycopg2.connect(connect_str)
        return conn

    except:
        logging.error('Failed to connect to database')
        return None

def validate_users(email : str, password : str) -> str:
    """
    Validates login credential for user
    :param email: user's email-id, e.g. abc@gmail.com
    :param password: user's password, e.g. howareyou
    :return: returns user_id if email and password matches. Else return string stating invalid
    """
    query = "select user_id from users where email='" + email + "' and password='" + password + "'";
    res = _execute_query(query)
    print("return value ",res)
    if res in none_list:
        logging.info("User not present")
        return "invalid"
    else:
        return res[0][0]


def register_users(name : str == "", email : str, password: str) -> bool:
    """
    Adds user's in database
    :param name : name of the user e.g. Mathur Villa
    :param email: user's email-id, e.g. mathurvilla@gmail.com
    :param password: user's password, e.g. bmw
    :return: returns true if user added successfully. Else return false indicating user already present.
    """
    query = "INSERT INTO users VALUES (\'{}\', \'{}\', \'{}\', \'{}\');"
    user_id = random_alnum("u_")
    query = query.format(user_id, name, email, password)
    res = _execute_query(query)

    if res in none_list:
        logging.info("User Already present")
        return False
    else:
        return True

if(__name__ == "__main__"):
    print("Ready")