# from flask import Flask, request, render_template
# import sqlite3

# app = Flask(__name__)

# # Function to search for papers in the database
# def search_papers(query):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ?",
#                    ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
#     results = cursor.fetchall()
#     conn.close()
#     return results

# @app.route("/", methods=["GET", "POST"])
# def search():
#     results = []
#     if request.method == "POST":
#         query = request.form["query"]
#         results = search_papers(query)  # Search for papers matching the query
#     return render_template("index.html", results=results)

# if __name__ == "__main__":
#     # app.run(debug=True)
#     app.run(debug=True, port=5001)


# step 4 
# from flask import Flask, request, render_template
# import sqlite3

# app = Flask(__name__)

# # Function to fetch papers based on the search query
# def get_papers(query):
#     # Connect to the database
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     # Search for papers based on the query term (searching by title or abstract)
#     cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ?", ('%' + query + '%', '%' + query + '%'))
#     papers = cursor.fetchall()

#     # Close the database connection
#     conn.close()

#     return papers

# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     papers = []

#     if query:
#         # Get papers matching the search query
#         papers = get_papers(query)

#     # Render the results in the HTML page
#     return render_template('index.html', papers=papers)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



# step 5

# from flask import Flask, request, render_template
# import sqlite3
# import math

# app = Flask(__name__)

# # Number of results per page
# PER_PAGE = 3

# # Function to fetch papers based on the search query with pagination
# def get_papers(query, page):
#     # Connect to the database
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     # Calculate the offset for the SQL query based on the page number
#     offset = (page - 1) * PER_PAGE

#     # Search for papers based on the query term (searching by title or abstract)
#     cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? LIMIT ? OFFSET ?", 
#                    ('%' + query + '%', '%' + query + '%', PER_PAGE, offset))
#     papers = cursor.fetchall()

#     # Get the total number of papers matching the query (for pagination)
#     cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ? OR abstract LIKE ?", 
#                    ('%' + query + '%', '%' + query + '%'))
#     total_results = cursor.fetchone()[0]
    
#     # Close the database connection
#     conn.close()

#     # Calculate the total number of pages
#     total_pages = math.ceil(total_results / PER_PAGE)

#     return papers, total_pages, page

# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     page = request.args.get('page', 1, type=int)  # Get the current page (default to 1)

#     papers = []
#     total_pages = 0

#     if query:
#         # Get papers and pagination details
#         papers, total_pages, page = get_papers(query, page)

#     # Render the results in the HTML page
#     return render_template('index.html', papers=papers, query=query, total_pages=total_pages, current_page=page)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



# # step 6 
# from flask import Flask, render_template, request
# import sqlite3

# app = Flask(__name__)

# # Connect to the database
# def get_db_connection():
#     conn = sqlite3.connect('papers.db')
#     conn.row_factory = sqlite3.Row  # Access rows as dictionaries
#     return conn

# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     # Set the number of results per page
#     results_per_page = 3
#     offset = (page - 1) * results_per_page

#     conn = get_db_connection()
#     cur = conn.cursor()

#     if search_by == 'title':
#         cur.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', results_per_page, offset))
#     elif search_by == 'author':
#         cur.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', results_per_page, offset))
#     elif search_by == 'date':
#         cur.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', results_per_page, offset))

#     papers = cur.fetchall()
#     conn.close()

#     # Get the total number of papers to calculate pagination
#     conn = get_db_connection()
#     cur = conn.cursor()

#     if search_by == 'title':
#         cur.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'author':
#         cur.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     elif search_by == 'date':
#         cur.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

#     total_results = cur.fetchone()[0]
#     conn.close()

#     total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page > 0 else 0)

#     return render_template('index.html', papers=papers, query=query, search_by=search_by, current_page=page, total_pages=total_pages)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



# # step 7 
# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to get all papers from the database
# def get_papers(query, search_by, page, per_page=5):
#     offset = (page - 1) * per_page
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     if search_by == 'title':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', per_page, offset))
#     elif search_by == 'author':
#         cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', per_page, offset))
#     elif search_by == 'date':
#         cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT ? OFFSET ?", ('%' + query + '%', per_page, offset))
    
#     papers = cursor.fetchall()
#     conn.close()
    
#     return papers

# # Function to get the total number of papers matching the query for pagination
# def get_total_papers(query, search_by):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     if search_by == 'title':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'author':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     elif search_by == 'date':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))
    
#     total_papers = cursor.fetchone()[0]
#     conn.close()
    
#     return total_papers

# # Route for paper detail view
# @app.route('/paper/<int:paper_id>')
# def paper_detail(paper_id):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
#     paper = cursor.fetchone()
#     conn.close()

#     paper_detail = {
#         'title': paper[1],
#         'abstract': paper[2],
#         'authors': paper[3],
#         'publication_date': paper[4]
#     }
#     return render_template('index.html', paper_detail=paper_detail)

# # Route for the main search page
# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))
    
#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate number of pages
    
#     return render_template('index.html', papers=papers, query=query, search_by=search_by, current_page=page, total_pages=total_pages)

# from flask import Flask, request, render_template
# import sqlite3

# app = Flask(__name__)

# # Get papers based on search query
# def get_papers(query, search_by, page=1):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     # Calculate the offset for pagination
#     offset = (page - 1) * 5

#     # Build the query based on search criteria
#     if search_by == 'title':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     elif search_by == 'authors':
#         cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     else:
#         cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))

#     papers = cursor.fetchall()
#     conn.close()
    
#     return papers

# # Get total number of papers matching the search
# def get_total_papers(query, search_by):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     if search_by == 'title':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'authors':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     else:
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

#     total_papers = cursor.fetchone()[0]
#     conn.close()
    
#     return total_papers

# # Home route for searching papers
# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate total number of pages
    
#     return render_template('index.html', papers=papers, query=query, search_by=search_by, current_page=page, total_pages=total_pages)

# # Paper detail route
# @app.route('/paper/<int:paper_id>')
# def paper_detail(paper_id):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
#     paper = cursor.fetchone()
#     conn.close()

#     if paper:
#         paper_detail = {
#             'title': paper[1],
#             'abstract': paper[2],
#             'authors': paper[3],
#             'publication_date': paper[4]
#         }
#         return render_template('paper_detail.html', paper=paper_detail)
#     else:
#         return "Paper not found", 404

# # if __name__ == '__main__':
# #     app.run(debug=True)


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


# from flask import Flask, request, render_template, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to get papers from the database based on search
# def get_papers(query, search_by, page=1):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     offset = (page - 1) * 5  # Pagination offset

#     # Build search query based on selection
#     if search_by == 'title':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     elif search_by == 'authors':
#         cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     else:
#         cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))

#     papers = cursor.fetchall()
#     conn.close()
#     return papers

# # Function to get total papers based on search
# def get_total_papers(query, search_by):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     if search_by == 'title':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'authors':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     else:
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

#     total_papers = cursor.fetchone()[0]
#     conn.close()
#     return total_papers

# # Route to display the home page and search results
# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate the total pages for pagination
    
#     return render_template('index.html', papers=papers, query=query, search_by=search_by, current_page=page, total_pages=total_pages)

# # Route for paper detail
# @app.route('/paper/<int:paper_id>')
# def paper_detail(paper_id):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
#     paper = cursor.fetchone()
#     conn.close()

#     if paper:
#         paper_detail = {
#             'title': paper[1],
#             'abstract': paper[2],
#             'authors': paper[3],
#             'publication_date': paper[4]
#         }
#         return render_template('paper_detail.html', paper=paper_detail)
#     else:
#         return "Paper not found", 404

# # Route to add new paper
# @app.route('/add_paper', methods=['POST'])
# def add_paper():
#     title = request.form['title']
#     abstract = request.form['abstract']
#     authors = request.form['authors']
#     publication_date = request.form['publication_date']

#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     cursor.execute("INSERT INTO papers (title, abstract, authors, publication_date) VALUES (?, ?, ?, ?)", 
#                    (title, abstract, authors, publication_date))
#     conn.commit()
#     conn.close()

#     # Redirect back to home page after adding the paper
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



#
# 
#  from flask import Flask, request, render_template, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to get papers from the database based on search
# def get_papers(query, search_by, page=1):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     offset = (page - 1) * 5  # Pagination offset

#     # Build search query based on selection
#     if search_by == 'title':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     elif search_by == 'authors':
#         cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     else:
#         cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))

#     papers = cursor.fetchall()
#     conn.close()
#     return papers

# # Function to get total papers based on search
# def get_total_papers(query, search_by):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     if search_by == 'title':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'authors':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     else:
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

#     total_papers = cursor.fetchone()[0]
#     conn.close()
#     return total_papers

# # Function to calculate Precision and Recall
# def calculate_precision_recall(query, search_by):
#     relevant_count = 0
#     retrieved_count = 0
#     total_relevant = get_total_papers(query, search_by)

#     papers = get_papers(query, search_by)
#     for paper in papers:
#         if query.lower() in paper[1].lower() or query.lower() in paper[2].lower():  # Checking in title or abstract
#             relevant_count += 1
#         retrieved_count += 1

#     precision = relevant_count / retrieved_count if retrieved_count else 0
#     recall = relevant_count / total_relevant if total_relevant else 0
#     return precision, recall

# # Route to display the home page and search results
# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate the total pages for pagination
    
#     # Calculate precision and recall for the query
#     precision, recall = calculate_precision_recall(query, search_by)

#     return render_template('index.html', papers=papers, query=query, search_by=search_by, 
#                            current_page=page, total_pages=total_pages, precision=precision, recall=recall)

# # Route for paper detail
# @app.route('/paper/<int:paper_id>')
# def paper_detail(paper_id):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
#     paper = cursor.fetchone()
#     conn.close()

#     if paper:
#         paper_detail = {
#             'title': paper[1],
#             'abstract': paper[2],
#             'authors': paper[3],
#             'publication_date': paper[4]
#         }
#         return render_template('paper_detail.html', paper=paper_detail)
#     else:
#         return "Paper not found", 404

# # Route to add new paper
# @app.route('/add_paper', methods=['POST'])
# def add_paper():
#     title = request.form['title']
#     abstract = request.form['abstract']
#     authors = request.form['authors']
#     publication_date = request.form['publication_date']

#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     cursor.execute("INSERT INTO papers (title, abstract, authors, publication_date) VALUES (?, ?, ?, ?)", 
#                    (title, abstract, authors, publication_date))
#     conn.commit()
#     conn.close()

#     # Redirect back to home page after adding the paper
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


# from flask import Flask, request, render_template, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to get papers from the database based on search
# def get_papers(query, search_by, page=1):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
    
#     offset = (page - 1) * 5  # Pagination offset

#     # Update search query to search across multiple fields if "keyword" is selected
#     if search_by == 'keyword':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ? LIMIT 5 OFFSET ?", 
#                        ('%' + query + '%', '%' + query + '%', '%' + query + '%', offset))
#     elif search_by == 'title':
#         cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     elif search_by == 'authors':
#         cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
#     else:
#         cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))

#     papers = cursor.fetchall()
#     conn.close()
#     return papers

# # Function to get total papers based on search
# def get_total_papers(query, search_by):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     if search_by == 'keyword':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ?", 
#                        ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
#     elif search_by == 'title':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
#     elif search_by == 'authors':
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
#     else:
#         cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

#     total_papers = cursor.fetchone()[0]
#     conn.close()
#     return total_papers

# # Function to calculate Precision and Recall
# def calculate_precision_recall(query, search_by):
#     relevant_count = 0
#     retrieved_count = 0
#     total_relevant = get_total_papers(query, search_by)

#     papers = get_papers(query, search_by)
#     for paper in papers:
#         if query.lower() in paper[1].lower() or query.lower() in paper[2].lower():  # Checking in title or abstract
#             relevant_count += 1
#         retrieved_count += 1

#     precision = relevant_count / retrieved_count if retrieved_count else 0
#     recall = relevant_count / total_relevant if total_relevant else 0
#     return precision, recall

# # Route to display the home page and search results
# @app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate the total pages for pagination
    
#     # Calculate precision and recall for the query
#     precision, recall = calculate_precision_recall(query, search_by)

#     return render_template('index.html', papers=papers, query=query, search_by=search_by, 
#                            current_page=page, total_pages=total_pages, precision=precision, recall=recall)

# # Route for paper detail
# @app.route('/paper/<int:paper_id>')
# def paper_detail(paper_id):
#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
#     paper = cursor.fetchone()
#     conn.close()

#     if paper:
#         paper_detail = {
#             'title': paper[1],
#             'abstract': paper[2],
#             'authors': paper[3],
#             'publication_date': paper[4]
#         }
#         return render_template('paper_detail.html', paper=paper_detail)
#     else:
#         return "Paper not found", 404

# # Route to add new paper
# @app.route('/add_paper', methods=['POST'])
# def add_paper():
#     title = request.form['title']
#     abstract = request.form['abstract']
#     authors = request.form['authors']
#     publication_date = request.form['publication_date']

#     conn = sqlite3.connect('papers.db')
#     cursor = conn.cursor()

#     cursor.execute("INSERT INTO papers (title, abstract, authors, publication_date) VALUES (?, ?, ?, ?)", 
#                    (title, abstract, authors, publication_date))
#     conn.commit()
#     conn.close()

#     # Redirect back to home page after adding the paper
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to get papers from the database based on search
def get_papers(query, search_by, page=1):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    
    offset = (page - 1) * 5  # Pagination offset

    # Update search query to search across multiple fields if "keyword" is selected
    if search_by == 'keyword':
        cursor.execute("SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ? LIMIT 5 OFFSET ?", 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', offset))
    elif search_by == 'title':
        cursor.execute("SELECT * FROM papers WHERE title LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
    elif search_by == 'authors':
        cursor.execute("SELECT * FROM papers WHERE authors LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))
    else:
        cursor.execute("SELECT * FROM papers WHERE publication_date LIKE ? LIMIT 5 OFFSET ?", ('%' + query + '%', offset))

    papers = cursor.fetchall()
    conn.close()
    return papers

# Function to get total papers based on search
def get_total_papers(query, search_by):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    if search_by == 'keyword':
        cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ? OR abstract LIKE ? OR authors LIKE ?", 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    elif search_by == 'title':
        cursor.execute("SELECT COUNT(*) FROM papers WHERE title LIKE ?", ('%' + query + '%',))
    elif search_by == 'authors':
        cursor.execute("SELECT COUNT(*) FROM papers WHERE authors LIKE ?", ('%' + query + '%',))
    else:
        cursor.execute("SELECT COUNT(*) FROM papers WHERE publication_date LIKE ?", ('%' + query + '%',))

    total_papers = cursor.fetchone()[0]
    conn.close()
    return total_papers

# Function to calculate Precision and Recall
# def calculate_precision_recall(query, search_by):
#     relevant_count = 0
#     retrieved_count = 0
#     total_relevant = get_total_papers(query, search_by)

#     papers = get_papers(query, search_by)
#     for paper in papers:
#         # Check if the paper contains the query in the relevant fields
#         if search_by == 'authors':
#             # We check if the query is present in the authors field
#             if query.lower() in paper[3].lower():  # Paper[3] is the authors field
#                 relevant_count += 1
#         elif query.lower() in paper[1].lower() or query.lower() in paper[2].lower():  # Paper[1] is title, Paper[2] is abstract
#             relevant_count += 1
        
#         retrieved_count += 1

#     precision = relevant_count / retrieved_count if retrieved_count else 0
#     recall = relevant_count / total_relevant if total_relevant else 0
#     return precision, recall

# Function to calculate Precision and Recall
def calculate_precision_recall_f1(query, search_by):
    relevant_count = 0
    retrieved_count = 0
    total_relevant = get_total_papers(query, search_by)

    papers = get_papers(query, search_by)
    for paper in papers:
        # Check if the paper contains the query in the relevant fields
        if search_by == 'authors':
            # We check if the query is present in the authors field
            if query.lower() in paper[3].lower():  # Paper[3] is the authors field
                relevant_count += 1
        elif search_by == 'publication_date':
            # We check if the query is present in the publication_date field
            if query.lower() in paper[4].lower():  # Paper[4] is the publication date field
                relevant_count += 1
        elif query.lower() in paper[1].lower() or query.lower() in paper[2].lower():  # Paper[1] is title, Paper[2] is abstract
            relevant_count += 1
        
        retrieved_count += 1

    precision = relevant_count / retrieved_count if retrieved_count else 0
    recall = relevant_count / total_relevant if total_relevant else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

# Route to display the home page and search results
@app.route('/', methods=['GET'])
# def index():
#     query = request.args.get('query', '')
#     search_by = request.args.get('search_by', 'title')
#     page = int(request.args.get('page', 1))

#     papers = get_papers(query, search_by, page)
#     total_papers = get_total_papers(query, search_by)
#     total_pages = (total_papers + 4) // 5  # Calculate the total pages for pagination
    
#     # Calculate precision and recall for the query
#     precision, recall = calculate_precision_recall(query, search_by)

#     return render_template('index.html', papers=papers, query=query, search_by=search_by, 
#                            current_page=page, total_pages=total_pages, precision=precision, recall=recall)
# Route to display the home page and search results
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', '')
    search_by = request.args.get('search_by', 'title')
    page = int(request.args.get('page', 1))

    papers = get_papers(query, search_by, page)
    total_papers = get_total_papers(query, search_by)
    total_pages = (total_papers + 4) // 5  # Calculate the total pages for pagination
    
    # Calculate precision, recall, and F1-score for the query
    precision, recall, f1_score = calculate_precision_recall_f1(query, search_by)

    return render_template('index.html', papers=papers, query=query, search_by=search_by, 
                           current_page=page, total_pages=total_pages, precision=precision, recall=recall, f1_score=f1_score)


# Route for paper detail
@app.route('/paper/<int:paper_id>')
def paper_detail(paper_id):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
    paper = cursor.fetchone()
    conn.close()

    if paper:
        paper_detail = {
            'title': paper[1],
            'abstract': paper[2],
            'authors': paper[3],
            'publication_date': paper[4]
        }
        return render_template('paper_detail.html', paper=paper_detail)
    else:
        return "Paper not found", 404

# Route to add new paper
@app.route('/add_paper', methods=['POST'])
def add_paper():
    title = request.form['title']
    abstract = request.form['abstract']
    authors = request.form['authors']
    publication_date = request.form['publication_date']

    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO papers (title, abstract, authors, publication_date) VALUES (?, ?, ?, ?)", 
                   (title, abstract, authors, publication_date))
    conn.commit()
    conn.close()

    # Redirect back to home page after adding the paper
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)


