import sqlite3

conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM papers")
papers = cursor.fetchall()

for paper in papers:
    print(paper)

conn.close()
