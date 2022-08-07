from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional

class LoginForm(Form):
    username = TextField('username', validators = [DataRequired()], render_kw = {"placeholder" : "Username"})
    password = TextField('password', validators = [DataRequired()], render_kw = {"placeholder" : "Password"})

class RegisterForm(Form):
    name = TextField('name', validators = [DataRequired()], render_kw = {"placeholder" : "First Name"})
    surname = TextField('surname', validators = [DataRequired()], render_kw = {"placeholder" : "Surname"})
    username = TextField('username', validators = [DataRequired()], render_kw = {"placeholder" : "Username"})
    password = TextField('password', validators = [DataRequired()], render_kw = {"placeholder" : "Password"})

class ResetForm(Form):
    username = TextField('username', validators = [DataRequired()], render_kw = {"placeholder" : "Username"})
    newpass = TextField('newpass', validators = [DataRequired()], render_kw = {"placeholder" : "New password"})

class EditForm(Form):
    name = TextField('name', validators = [Optional()], render_kw = {"placeholder" : "Change your name"})
    surname = TextField('surname', validators = [Optional()], render_kw = {"placeholder" : "Change your surname"})
    description = TextAreaField('description', validators = [Optional()], render_kw = {"placeholder" : "Your personal information"})

class PostForm(Form):
    description = TextAreaField('description', validators = [DataRequired()], render_kw = {"placeholder" : "Share some of your thoughts"})
