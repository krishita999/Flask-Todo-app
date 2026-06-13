from flask import Flask, render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key='krishita'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return f"{self.SNo} {self.title}"


@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        title= request.form['title']
        desc = request.form["desc"]
        todo = Todo(title=title,desc = desc)
        db.session.add(todo)
        db.session.commit()
        flash("Todo Added Successfully!","success")
        return redirect("/")
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo = allTodo)

@app.route("/update/<int:SNo>",methods = ["GET","POST"])
def Update(SNo):
     todo = Todo.query.filter_by(SNo=SNo).first()
     if request.method == "POST":
        title= request.form['title']
        desc = request.form["desc"]

        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        flash("Todo Updated Successfully!","warning")
        return redirect("/")
     return render_template("update.html",todo=todo)
    
     

@app.route("/delete/<int:SNo>")
def Delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo Deleted Successfully!","danger")
    return redirect("/")

@app.route("/about")
def about():

    return render_template("about.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
