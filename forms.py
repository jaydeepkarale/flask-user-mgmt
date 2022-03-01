from wtforms import Form, BooleanField, StringField, PasswordField, validators

class UserRegisterForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=100)])
    email = StringField('Email Address', [validators.Length(max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Repeat Password')

class UserLoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=100)])    
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password2', message='Passwords must match')
    ])
    
    
