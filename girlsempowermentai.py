from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13384@October2",
    database="girlsempowermentai"
)
cursor = db.cursor(dictionary=True)

# User Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name, email, password = data['name'], data['email'], data['password']
    hashed_pw = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    
# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data['email'], data['password']

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }})
    return jsonify({"message": "Invalid credentials"}), 401

# Nutrition Suggestion
@app.route('/nutrition', methods=['POST'])
def add_nutrition():
    data = request.json
    cursor.execute("INSERT INTO nutrition (user_id, meal, suggestion) VALUES (%s, %s, %s)", 
                   (data['user_id'], data['meal'], data['suggestion']))
    db.commit()
    return jsonify({"message": "Nutrition suggestion added"})

@app.route('/nutrition/<int:user_id>', methods=['GET'])
def get_nutrition(user_id):
    cursor.execute("SELECT * FROM nutrition WHERE user_id=%s", (user_id,))
    return jsonify(cursor.fetchall())

# Health Advice
@app.route('/health', methods=['POST'])
def add_health():
    data = request.json
    cursor.execute("INSERT INTO health (user_id, condition, advice) VALUES (%s, %s, %s)", 
                   (data['user_id'], data['condition'], data['advice']))
    db.commit()
    return jsonify({"message": "Health advice added"})

@app.route('/health/<int:user_id>', methods=['GET'])
def get_health(user_id):
    cursor.execute("SELECT * FROM health WHERE user_id=%s", (user_id,))
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)
