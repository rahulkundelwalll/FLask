from flask import Flask, render_template,jsonify,request
import sqlite3
from datetime import datetime

app = Flask(__name__)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                sno INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                date_create DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        self.conn.close()

@app.route('/add',methods=['POST'])
def add_todo():
    try:
        # Get JSON data from the request
        title = request.json.get('title')
        description = request.json.get('description')

        # Check if required fields are present
        if not title or not description:
            return jsonify({"error": "Title and Description are required"}), 400

        # Database connection
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        
        # Insert data into the todo table
        c.execute("INSERT INTO todo (title, description) VALUES (?, ?)", (title, description))
        conn.commit()

        return jsonify({"message": "Todo item added successfully", "id": c.lastrowid}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except sqlite3.OperationalError as e:
        return jsonify({"error": "Database operation failed", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    finally:
        # Ensure database connection is closed
        conn.close()

@app.route('/get', methods=['GET'])
def get_todo():
    try:
        # Connect to the database
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        
        # Fetch all todos
        c.execute("SELECT * FROM todo")
        todos = c.fetchall()  # Fetch all rows

        # Convert to a list of dictionaries
        todo_list = []
        for row in todos:
            todo_list.append({
                "sno": row[0],
                "title": row[1],
                "description": row[2],
                "date_create": row[3]
            })

        return jsonify({"message": "Todos fetched successfully", "data": todo_list}), 200

    except sqlite3.OperationalError as e:
        return jsonify({"error": "Database operation failed", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    finally:
        conn.close() 


@app.route('/products')
def product():
    return "I am product"

if __name__ == "__main__":
    Database()
    app.run(debug=True, port=8000)
