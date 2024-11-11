import sqlite3

def search_papers(query):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ?",
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    print(f"Results from DB: {results}")  # Debugging line to print results from the DB
    conn.close()
    return results
    # print(results)
