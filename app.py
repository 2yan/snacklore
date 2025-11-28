from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/snacklore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and initialized.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            
    app.run(host='0.0.0.0', port=5000, debug=True)
