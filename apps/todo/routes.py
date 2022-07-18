from apps.todo import bp
from apps import db
from apps.models import Todo

@bp.route("/todos",methods=['GET'])
def hello_world():
    return "<p>Hi, this is todo page</p>"


@bp.route("/create",methods=['GET'])
def create():
    todo = Todo(description="this is description", active=True)
    db.session.add(todo)
    db.session.commit()
    return "you just create new data, please check database"


@bp.route("/read",methods=['GET'])
def read():
    todos = Todo.query.all()
    todo_data = []
    for todo in todos:
        todo_data.append({
            "id" : todo.id,
            "description" : todo.description            
            })
    return str(todo_data)


@bp.route("/update/<todo_id>",methods=['GET'])
def update(todo_id):
    try :
        todo = Todo.query.filter_by(id=int(todo_id)).first()
        if todo :
            todo.description = "Yeay update function is working"
            db.session.commit()
            return "you just update the data, please check database"
        else :
            return f"cannot find data with id {todo_id}"
    except Exception as e:
        return "something not right"


@bp.route("/delete/<todo_id>",methods=['GET'])
def delete(todo_id):
    try :
        todo = Todo.query.filter_by(id=int(todo_id))
        if todo :
            todo.delete()
            db.session.commit()
            return "you just delete a data, please check database"
        else :
            return f"cannot find data with id {todo_id}"
    except Exception as e:
        return "something not right"
