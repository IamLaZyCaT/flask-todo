from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

# Database configuration (SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Create a model (table structure)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return f"<Task {self.id} - {self.heading}>"

# Create the database file (once)
with app.app_context():
    db.create_all()

# temporary in-memory list to store tasks
# tasks= []

@app.route("/")
def home():
     # Fetch all tasks from database
    tasks = Task.query.order_by(Task.date_created.desc()).all()
    # this renders the HTML page and passes current tasks to it
    return render_template('index.html', tasks = tasks)

@app.route('/add',methods=['POST'])
def addTask():
    heading=request.form.get('heading')
    content=request.form.get('content')

    # store it in list (temporary, will later connect to DB)
    if heading and content:
        new_task = Task(heading=heading, content=content)
        db.session.add(new_task)
        db.session.commit()
      
        
    return redirect('/')

@app.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

    


if __name__=="__main__":
    app.run(debug=True)