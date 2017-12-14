from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import *
from models import *
import json

import hashlib, os, base64

app = Flask(__name__)
app.secret_key = 'iwnvasfhieunga;fogenabsu12nfpfa;ga[gjiajsgashj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.sqlite'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You need to be logged in to do that!')
    return redirect('/login')

@app.route('/')
def index():
    return "Welcome to Flask"+("<br>"*15)+"built by tristan termini 2017"

@app.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash('A user of that email address already exists!')
                return redirect(url_for('register'))
            else:
                pasw = form.password.data
                passhash = bcrypt.generate_password_hash(pasw).decode('utf8')
                newuser = User(form.email.data,passhash)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                flash("New user was created and logged in!")
                return redirect(url_for('register'))
        else:
            return str(form.errors)

@app.route('/login',methods=['GET','POST'])
def login():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                pasw = form.password.data
                hashcheck = bcrypt.check_password_hash(user.password,pasw)
                if hashcheck:
                    login_user(user)
                    flash("Logged in!")
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect Password!")
                    return redirect(url_for('login'))
            else:
                flash("No user with that email address exists!")
                return redirect(url_for('login'))
        else:
            return str(form.errors)

@app.route("/quiz",methods=['GET','POST'])
@login_required
def quiz():
    if request.method=='GET':
        return render_template('quiz.html')
        pass
    elif request.method=='POST':
        print(request.form)
        f = None
        q = {}
        for value in request.form.keys():
            if (value.startswith('quiz')):
                print("loading quiz "+ value[4:])
                f = json.load(open("static/ajax/"+value+".json"))
            else:
                print(value + "::"+ request.form.get(value))
                q[value] = request.form.get(value)

        score = 0
        scoresize = len(q.keys())
        for answer in q.keys():
            print(f['questions'][int(answer)]['a'][int(q.get(answer))])
            if f['questions'][int(answer)]['a'][int(q.get(answer))]['correct'] == 'true':
                score += 1
        print("Scored: " + str(int((score/scoresize)*100))+"%")
        return render_template('quiz.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"

@app.route('/profile')
@login_required
def profile_non():
    return redirect('/profile/'+current_user.email)

@app.route('/profile/<email>')
@login_required
def profile(email):
    usr = User.query.filter_by(email=email).first()
    if (usr != None):
        return render_template('profile.html', user=usr)
    else:
        return ('No profile here.')

@app.route('/my-profile')
@login_required
def my_profile():
    return redirect('/profile/'+current_user.email)
    #return render_template('profile.html',user=current_user)


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)
