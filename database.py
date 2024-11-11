import sqlite3

# Create a connection to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

# Create the papers table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    authors TEXT,
    publication_date TEXT
)
''')

# Sample data for 10 papers
sample_papers = [
    ("Deep Learning for Fish Detection", "A study on using deep learning to detect fish in underwater environments.", "John Doe, Jane Smith", "2023-10-15"),
    ("Marine Biology Insights", "Research on marine ecosystems and biodiversity.", "Alice Johnson, Bob Brown", "2022-07-22"),
    ("Aquaculture and AI", "Exploring the role of AI in aquaculture for efficient farm management.", "Sara Lee, Mike Davis", "2024-01-30"),
    ("AI in Fish Farming", "Application of artificial intelligence in the optimization of fish farming processes.", "Tom White, Maria Green", "2021-05-10"),
    ("Underwater Robotics for Fish Tracking", "Development of underwater robots for tracking marine life.", "Paul Allen, Lisa Black", "2020-11-25"),
    ("Fish Behavior Prediction with AI", "Using machine learning to predict fish behavior in aquaculture.", "Javier Perez, Natalie Blue", "2023-03-18"),
    ("Sustainable Aquaculture Practices", "Research on sustainable practices in fish farming.", "Gina Black, Leo White", "2022-06-05"),
    ("Impact of Climate Change on Fish Populations", "Examining how climate change affects fish populations.", "Mark Gray, Sylvia Green", "2021-12-01"),
    ("Advanced Algorithms for Fish Detection", "Exploring advanced algorithms to detect fish in complex environments.", "Kurt Rich, Helen Lee", "2023-08-22"),
    ("The Future of Aquaculture", "Looking ahead at the role of technology in the future of fish farming.", "John Blue, Emma Green", "2024-02-14")
]

# Insert the sample papers into the database
cursor.executemany("INSERT INTO papers (title, abstract, authors, publication_date) VALUES (?, ?, ?, ?)", sample_papers)
conn.commit()

# Close the connection to the database
conn.close()

print("Database and sample papers created successfully!")



# import sqlite3
# conn = sqlite3.connect('papers.db')
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM papers")  # This retrieves all rows from the 'papers' table
# rows = cursor.fetchall()

# for row in rows:
#     print(row)  # This will print each row in the table

# conn.close()

