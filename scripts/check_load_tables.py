import psycopg2

con = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='postgres')
cur = con.cursor()

sql = """
    SELECT
        table_schema || '.' || table_name
    FROM
        information_schema.tables
    WHERE
        table_type = 'BASE TABLE'
    AND
        table_schema NOT IN ('pg_catalog', 'information_schema');
"""

cur.execute(sql)
con.commit()

recset = cur.fetchall()
for rec in recset:
    print (rec)

con.close()
