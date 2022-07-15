from apps.todo import bp

@bp.route("/todos")
def hello_world():
    return "<p>Hi, this is todo page</p>"