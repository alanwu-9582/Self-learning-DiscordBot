import sqlite3

DATABASE = "RuruhimeLearningData.db" 
TABLE = "LearningData"

conn = sqlite3.connect(DATABASE)
m_cursor = conn.cursor()

m_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE} (
    keyword varchar(128) NOT NULL,
    response varchar(128) NOT NULL
);''')
conn.commit()

m_cursor.execute(f"DELETE from {TABLE} where keyword = 'Hello';")
m_cursor.execute(f"INSERT INTO {TABLE} VALUES ('Hello', 'World !')")
conn.commit()

m_cursor = m_cursor.execute(f"SELECT * from {TABLE}")
for row in m_cursor:
    print(row)

conn.commit()
m_cursor.close()
conn.close()