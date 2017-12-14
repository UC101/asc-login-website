from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(80),primary_key=True,unique=True)
    password = db.Column(db.String(80))
    #Controls whether they are marking or answering questions
        #0 == answering, 1 == marking
        #Every five questions answered, TaskCompleteCount must be marked and vice versa
    task = db.Column(db.Integer(),default=0)
    task_count = db.Column(db.Integer())
    performance = db.Column(db.Integer(),default=0)

    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.task = 0
        self.task_count = 10
        self.performance = 0

    def __repr__(self):
        return '<User %r>' % self.email

    def switch_modes(self):
        task_count = 10
        if task == 0:
            task = 1
        else:
            task = 0

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)


class Answered(db.Model):
    uid = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    owner = db.Column(db.String(80)) #email of whoever answered it
    question = db.Column(db.String(100)) #question given
    answer = db.Column(db.String(140)) #answered question
    taken = db.Column(db.String(80)) #email of whoever has been assigned, none by defualt

    def __init__(self,owner,quest,answer):
        self.owner = owner
        self.question = quest
        self.answer = answer
        self.taken = 'none'

    def __repr__():
        return '<Answered %r>' % self.owner
