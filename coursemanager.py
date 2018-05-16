import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "coursedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    par = db.Column(db.Integer)

    def __repr__(self):
        return "<Title: {}>".format(self.body)

    @app.route("/", methods=["GET", "POST"])
    def home():
        courses = None
        if request.form:
            try:
                course = Course(name=request.form.get("name"), location=request.form.get("location"), par=request.form.get("par"))
                db.session.add(course)
                db.session.commit()
            except Exception as e:
                print("Failed to add course")
                print(e)
                return redirect("/")
        courses = Course.query.all()
        return render_template("home.html", courses=courses)

    @app.route("/update", methods=["POST"])
    def update():
        try:
            newname = request.form.get("newname")
            oldname = request.form.get("oldname")
            course = Course.query.filter_by(name=oldname).first()
            course.name = newname
            newlocation = request.form.get("newlocation")
            oldlocation = request.form.get("oldlocation")
            course = Course.query.filter_by(location=oldlocation).first()
            course.location = newlocation
            newpar = request.form.get("newpar")
            oldpar = request.form.get("oldpar")
            course = Course.query.filter_by(par=oldpar).first()
            course.par = newpar
            db.session.commit()
        except Exception as e:
            print("Couldn't update course")
            print(e)
        return redirect("/")

    @app.route("/delete", methods=["POST"])
    def delete():
        name = request.form.get("name")
        course = Course.query.filter_by(name=name).first()
        db.session.delete(course)
        db.session.commit()
        return redirect("/")

# class end
if __name__ == "__main__":
    app.run(debug=True)
