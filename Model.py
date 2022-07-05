
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length

class Login(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=6,max=64)])
    password = PasswordField(validators=[InputRequired(),Length(min=6,max=64)])
    submit = SubmitField()

class Register(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=6,max=64)])
    password = PasswordField(validators=[InputRequired(),Length(min=6,max=64)])
    password_re = PasswordField(validators=[InputRequired(),Length(min=6,max=64)])
    submit = SubmitField()