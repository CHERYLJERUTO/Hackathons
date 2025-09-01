from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="13384@October2",
            database="girlsempowermentai",
            autocommit=True
        )
        return db
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# User Signup
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name, email, password = data['name'], data['email'], data['password']
        
        # Validate input
        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400
        
        hashed_pw = generate_password_hash(password)
        
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({"error": "User already exists"}), 409
        
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                      (name, email, hashed_pw))
        cursor.close()
        db.close()
        
        return jsonify({"message": "User registered successfully"}), 201
        
    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email, password = data['email'], data['password']
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            # Don't send password back to frontend
            user_data = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
            return jsonify({"message": "Login successful", "user": user_data}), 200
        
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

# Add Nutrition Suggestion
@app.route('/nutrition', methods=['POST'])
def add_nutrition():
    try:
        data = request.json
        user_id, meal, suggestion = data['user_id'], data['meal'], data['suggestion']
        
        if not all([user_id, meal, suggestion]):
            return jsonify({"error": "All fields are required"}), 400
        
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO nutrition (user_id, meal, suggestion) VALUES (%s, %s, %s)", 
                      (user_id, meal, suggestion))
        cursor.close()
        db.close()
        
        return jsonify({"message": "Nutrition suggestion added successfully"}), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to add nutrition: {str(e)}"}), 500

# Get Nutrition Suggestions
@app.route('/nutrition/<int:user_id>', methods=['GET'])
def get_nutrition(user_id):
    try:
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nutrition WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        nutrition_data = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(nutrition_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get nutrition data: {str(e)}"}), 500

# Add Health Advice
@app.route('/health', methods=['POST'])
def add_health():
    try:
        data = request.json
        user_id, condition, advice = data['user_id'], data['condition'], data['advice']
        
        if not all([user_id, condition, advice]):
            return jsonify({"error": "All fields are required"}), 400
        
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO health (user_id, condition, advice) VALUES (%s, %s, %s)", 
                      (user_id, condition, advice))
        cursor.close()
        db.close()
        
        return jsonify({"message": "Health advice added successfully"}), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to add health advice: {str(e)}"}), 500

# Get Health Advice
@app.route('/health/<int:user_id>', methods=['GET'])
def get_health(user_id):
    try:
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM health WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        health_data = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(health_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get health data: {str(e)}"}), 500

# Test endpoint
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend is running successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)