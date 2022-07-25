from apps.todo import bp
from apps import db
from apps.models import Todo ,Tag
from flask import redirect, render_template, request, url_for
from apps.todo.forms import TodoForm, TagForm
from flask_login import login_required,current_user

@bp.route("/",methods=['GET','POST'])
@bp.route("/index",methods=['GET','POST'])
@login_required
def index():
    form = TodoForm()
    # filter data tag by current user
    form.set_tags_choices(current_user) #running this function set all data tags in tag fields.
    if form.validate_on_submit(): #we will check if form is validate or not
        date_todo = form.date_todo.data
        if date_todo :
            date_todo = date_todo.utcnow() #for date_todo we want to strore data in utc
        tags = db.session.query(Tag).filter(Tag.id.in_(form.tags.data)).all() #search all tag data object based on tag id when user select on form
        todo = Todo(description=form.description.data,date_todo=date_todo,tags=tags,author=current_user)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))

    todos = Todo.query.filter_by(active=True,user_id=current_user.id).all() #get all todo from database and parse it to html and render
    return render_template("todo/index.html",todos=todos,title="Todos",form=form)



@bp.route("/set_active_todo/<todo_id>",methods=['POST'])
@login_required
def set_active_todo(todo_id): #parsing todo id in route
    todo = Todo.query.get(todo_id) #get todo object based on todo id
    if todo.active: #if todo active = true, we will set it active = false and vice versa
        todo.active = False
    else :
        todo.active = True
    db.session.commit() #commit to database
    return redirect(request.referrer) #this will return to url before user hit url set_active_todo because we want refirect to the sampe page before user hit this button


@bp.route("/delete_todo/<todo_id>",methods=['POST'])
@login_required
def delete_todo(todo_id):
    Todo.query.filter_by(id=todo_id).delete() #get todo object base on todo id and delete    
    db.session.commit() #commit to database
    return redirect(request.referrer) #this will return to url before user hit url delete_todo because we want refirect to the sampe page before user hit this button
    
@bp.route("/todo_archive",methods=['GET'])
@login_required
def todo_archive():
    todos = Todo.query.filter_by(active=False,user_id=current_user.id).all() #get all todo from database and parse it to html and render
    return render_template("todo/index.html",todos=todos,title="Archive")


@bp.route("/tags",methods=['GET','POST'])
@login_required
def get_tags():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data,tag_user=current_user)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('todo.get_tags'))

    tags = current_user.tags.all()
    return render_template("todo/tags.html",tags=tags,title="Tags",form=form)


@bp.route("/delete_tag/<tag_id>",methods=['POST'])
@login_required
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete() #get todo object base on todo id and delete    
    db.session.commit() #commit to database
    return redirect(request.referrer) #this will return to url before user hit url delete_todo because we want refirect to the sampe page before user hit this button
    