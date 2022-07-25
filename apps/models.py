from apps import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# identify current user login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#tags table, table many2many relation for todo and tag
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id',ondelete="CASCADE"), primary_key=True),
    db.Column('todo_id', db.Integer, db.ForeignKey('todo.id',ondelete="CASCADE"), primary_key=True)
)
#ondelete cascade means when we delete todo or tag, it will automatically delete the data in many2many table too.

class Todo(db.Model): #class name will be convert to table name
    # __tablename__ = 'table_name' # uncomment this if you want to have custom table name
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    date_todo = db.Column(db.DateTime, index=True)
    active = db.Column(db.Boolean, default=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('post', lazy=True)) #many2many to table tag
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #many2one to user table

    def __repr__(self):
        return '<Todo {}>'.format(self.description) #this will represent the data when we browse it, <Todo desscription>

class User(UserMixin,db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    todos = db.relationship('Todo', backref='author', lazy='dynamic') #one2many to table todo, author will be the alias
    tags = db.relationship('Tag', backref='tag_user', lazy='dynamic') #one2many to table tag, tag_user will be the alias

    def __repr__(self):
        return '<User {}>'.format(self.username)

    #set hash password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    #compare row password and hash password
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #many2one to table user

    def __repr__(self):
        return '<Tag {}>'.format(self.name)