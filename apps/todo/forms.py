from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectMultipleField,DateTimeLocalField,StringField
from wtforms.validators import Optional
from apps.models import Tag


#define class form for todo
class TodoForm(FlaskForm):
    description = TextAreaField('Description',render_kw={"placeholder": "Todo"})
    tags = SelectMultipleField('Tags',render_kw={"placeholder": "Tags"},coerce=int)
    date_todo = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M',validators=[Optional()])
    submit = SubmitField('Submit')

    #function to set tags value in form, we will search all data from tag table
    def set_tags_choices(self):        
        self.tags.choices = [(d.id, d.name) for d in Tag.query.all()]

class TagForm(FlaskForm):
    name = StringField('Tag',render_kw={"placeholder": "Tag"})
    submit = SubmitField('Submit')