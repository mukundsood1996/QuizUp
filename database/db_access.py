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
    connect_str = "dbname='quizup' user='sood' host='localhost' password='sood'"
    # connect_str = "dbname='quizup' user='postgres' host='localhost' password='welcomeback'"
    # connect_str = "dbname='quizup' user='postgres' host='localhost' password='postgres'"

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
    query = "SELECT user_id, name FROM users WHERE email='" + email + "' and password='" + password + "'";
    res = _execute_query(query)
    print("return value ",res)
    if res in none_list:
        logging.info("User not present")
        return "invalid"
    else:
        return res[0]


def register_users(name : str == "", email: str, password: str) -> bool:
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
        logging.info("User already present")
        return False
    else:
        return True

def get_user(user_id : str):
    """
    Gets user name given then user's ID
    :param user_id: gives us of the user e.g. u_AbcD
    """
    query = "SELECT name FROM users WHERE user_id='" + user_id + "'"
    res = _execute_query(query)
    print("return value", res)
    if res in none_list:
        logging.info("User does not exist")
        return "invalid"
    else:
        return res[0][0]


def get_questions(quiz_id : str):
    """
    Gets all questions of a particular quiz
    :param quiz_id: gives us the quiz the user wants to take
    """
    query = "SELECT * FROM question WHERE quiz_id='" + quiz_id + "'"
    res = _execute_query(query)
    print("\n\n\n\n\n\n\n\nreturn value", res)
    if res in none_list:
        logging.info("No questions")
        return "invalid"
    else:
        return res

def get_num_questions(quiz_id : str):
    """
    Get the number of questions in that quiz
    :param quiz_id: gives us the quiz the user wants to take
    """
    query = "SELECT num_questions FROM quiz WHERE quiz_id='" + quiz_id + "'"
    res = _execute_query(query)
    print('return value', res)
    if res in none_list:
        logging.info("No quiz")
        return "invalid"
    else:
        return res


if(__name__ == "__main__"):
    print("Ready")

