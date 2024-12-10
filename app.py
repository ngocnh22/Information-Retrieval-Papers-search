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



