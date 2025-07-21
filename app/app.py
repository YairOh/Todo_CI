import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Load database configuration from environment variables
DB_HOST = os.environ.get("DB_HOST", "db")  # Default to 'db' since Docker Compose names it as such
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "todo")

# Configure SQLAlchemy connection to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def days_until_deadline(self):
        """Calculate the number of days until the deadline."""
        if not self.deadline:
            return float('inf')
        return (self.deadline - datetime.now().date()).days

    def status_color(self):
        """Determine the color based on task completion and proximity to deadline."""
        if self.completed:
            return 'green'
        if not self.deadline:
            return 'orange'
        days_left = self.days_until_deadline()
        if days_left <= 1:
            return 'red'
        elif days_left <= 3:
            return 'orange'
        return 'white'

# Create tables in the database if they don't exist
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'task' in request.form:
            deadline = None
            if 'deadline' in request.form and request.form['deadline']:
                deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()
            new_task = Task(description=request.form['task'], deadline=deadline)
            db.session.add(new_task)
            db.session.commit()

        elif 'complete' in request.form:
            task_id = request.form['complete']
            task = Task.query.get(task_id)
            if task:
                task.completed = not task.completed
                db.session.commit()

        elif 'delete' in request.form:
            task_id = request.form['delete']
            task = Task.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()

        return redirect(url_for('index'))

    tasks = Task.query.all()
    sorted_tasks = sorted(
        tasks,
        key=lambda x: (x.completed, x.deadline is None, x.deadline or datetime.max.date())
    )
    
    return render_template('index.html', tasks=sorted_tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
