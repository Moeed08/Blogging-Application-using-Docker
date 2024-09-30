from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="postgres",  
            database="blogdb",
            user="bloguser",
            password="blogpass"
        )
        return conn
    except Exception as e:
        print(f"Facing error with connecting to the database: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS blogposts (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return "Welcome to the Blog Application"
@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"Error!": "Database connection has failed"}), 500
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM blogposts;')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    new_post = request.json.get('content')
    if not new_post:
        return jsonify({"error": "Content is required"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection has failed"}), 500
    
    cur = conn.cursor()
    cur.execute('INSERT INTO blogposts (content) VALUES (%s)', (new_post,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Post created successfully"}), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    updated_content = request.json.get('content')
    if not updated_content:
        return jsonify({"error": "Content is required"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection has failed"}), 500
    
    cur = conn.cursor()
    cur.execute('UPDATE blogposts SET content = %s WHERE id = %s', (updated_content, post_id))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Blog Post updated successfully"}), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute('DELETE FROM blogposts WHERE id = %s', (post_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Blog Post deleted successfully"}), 200

if __name__ == '__main__':
    init_db() 
    app.run(host='0.0.0.0', port=5000)