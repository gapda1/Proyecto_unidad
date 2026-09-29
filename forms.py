from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegisterForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=50,
                message="El usuario debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email(message="Ingresa un correo válido.")
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=6,
                message="La contraseña debe tener al menos 6 caracteres."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Las contraseñas deben coincidir."
            )
        ]
    )

    submit = SubmitField("Registrar")


class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Iniciar sesión")


class EditUserForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField("Guardar cambios")