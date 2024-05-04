from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired(), Length(min=5, max=25)])
    email = StringField("Почта", validators=[InputRequired()])
    password_1 = PasswordField("Пароль", validators=[InputRequired(), Length(min=5, max=25)])
    password_2 = PasswordField("Повторите пароль", validators=[InputRequired(), Length(min=5, max=25)])
    submit = SubmitField('Зарегистрироваться', id='submit-btn')

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired(), Length(min=5, max=25)])
    password = PasswordField("Пароль", validators=[InputRequired(), Length(min=5, max=25)])
    submit = SubmitField('Войти', id='submit-btn')
