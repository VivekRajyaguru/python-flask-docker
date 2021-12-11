from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return "<Task %r>" % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDO(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            print("Error While Saving Data in Database")
            return "Error While Saving Data in Database"
    else:
        tasks = ToDO.query.order_by(ToDO.date_created).all()
        print("Tasks ", tasks)
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDO.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        print("Error While Deleting Object")
        return "Error While Deleting Object"

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    try:
        task = ToDO.query.get_or_404(id)
        if request.method == 'POST':
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        else:
            return render_template('update.html', task = task)
    except:
        print("Error While Updating")
        return "Error While Updating"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)