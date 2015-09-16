from wtforms import Form, StringField, BooleanField, validators

class addPostForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=500)])
    text = StringField('Text')