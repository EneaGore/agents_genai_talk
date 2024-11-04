import sqlite3
import pandas as pd
class ScoreDatabase:
    def __init__(self, db_name="my.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Private method to ensure the scores table is created."""
        with sqlite3.connect(self.db_name) as conn:
            create_table = """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                submissionId INTEGER NOT NULL,
                submission TEXT NOT NULL,
                score INT
            );
            """
            cursor = conn.cursor()
            cursor.execute(create_table)
            conn.commit()
    
    def show_scores(self):
        """Displays all records from the scores table."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scores")
            records = cursor.fetchall()
            return records 

    def insert_score(self, submissionId, submission, score):
        """Inserts a new record into the scores table."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scores (submissionId, submission, score) VALUES (?, ?, ?)",
                (submissionId, submission, score)
            )
            conn.commit()
            
    def fetch_scores_from_db():
        conn = sqlite3.connect('my.db')  
        query = "SELECT submissionId, score FROM scores"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df