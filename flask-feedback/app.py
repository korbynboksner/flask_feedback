from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bycrypt
from models import db, connect_db, User, Feedback
from flask_sqlalchemy import SQLAlchemy
from forms import AddUserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adpot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route("/")
def homepage():

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    form = AddUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name,pwd,email,first_name,last_name)
        db.session.add(user)
        db.session.commit()

        session["username"]= user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if "username" in session:
        return redirect(f"/users/{session['username']}")


    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        if user: 
            session["username"] = user.username
            return redirect("/users/<username>")
        else: 
            form.username.errors = ["bad name/password"]
    return render_template("login.html", form=form)

@app.route("/users/<username>", methods=['GET'])
def userdisplay(username):
    if "username" not in session or username != session['username']:
        flash("you must be logged in to view!")
        return redirect("/")
    else:
        user= User.query.get_or_404(username)
        return render_template("user.html", user=user)

@app.route("/logout")
def logout():

    session.pop("user_id")

    return redirect("/")

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    if "username" not in session or username != session['username']: 
        flash("you must be logged in to view!")
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    form = FeedbackForm()
    if "username" not in session or username != session['username']:
        flash("you must be logged in to view!")
        return redirect("/")
    else: 
        if form.validate_on_submit():
            title = form.title.data
            content =form.content.data

            feedback= Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()

            return redirect(f"/users/{feedback.username}")

        else: 
            return render_template("feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("you must be logged in to view!")
        return redirect("/")
    else: 
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.commit()

            return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("you must be logged in to view!")
        return redirect("/")
    else:
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")