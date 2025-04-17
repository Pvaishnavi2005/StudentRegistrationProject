from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'student_db'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'postgres-service')
    )

# Create students table if it doesn't exist
with get_db_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                grade VARCHAR(10) NOT NULL
            );
        """)
        conn.commit()

@app.route('/register', methods=['POST'])
def register_student():
    data = request.get_json()
    student_id = data.get('student_id')
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    if not all([student_id, name, age, grade]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Check for duplicate student_id
                cur.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))
                if cur.fetchone():
                    return jsonify({'error': 'Student ID already exists'}), 400
                
                # Insert new student
                cur.execute(
                    "INSERT INTO students (student_id, name, age, grade) VALUES (%s, %s, %s, %s)",
                    (student_id, name, age, grade)
                )
                conn.commit()
        return jsonify({'message': 'Student registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)