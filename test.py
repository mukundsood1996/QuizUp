import psycopg2

try:
    connect_str = "dbname=pricing_list user=postgres password=sood"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    cursor.execute("""CREATE TABLE tutorials (name char(40));""")
    cursor.execute("""INSERT INTO tutorials VALUES ('Mukund');""")
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from tutorials""")
    rows = cursor.fetchall()
    print(rows)
    conn.commit()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)