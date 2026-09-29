from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from functools import wraps

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db
from models.user import User

from forms import (
    RegisterForm,
    LoginForm,
    EditUserForm
)


users_bp = Blueprint(
    "users",
    __name__
)


def login_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            flash(
                "Debes iniciar sesión primero.",
                "error"
            )

            return redirect(
                url_for("users.login")
            )

        return func(*args, **kwargs)

    return decorated_function



@users_bp.route("/")
def index():

    usuarios = User.query.all()

    return render_template(
        "user_list.html",
        usuarios=usuarios
    )


@users_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        usuario_existente = User.query.filter_by(
            email=form.email.data
        ).first()

        if usuario_existente:
            flash(
                "El correo electrónico ya está registrado.",
                "error"
            )

            return render_template(
                "register.html",
                form=form
            )

        nuevo_usuario = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data
            )
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(
            "Usuario registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("users.login")
        )

    return render_template(
        "register.html",
        form=form
    )


@users_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    form = LoginForm()

    if form.validate_on_submit():

        usuario = User.query.filter_by(
            email=form.email.data
        ).first()

        if usuario and check_password_hash(
            usuario.password,
            form.password.data
        ):

            session["user_id"] = usuario.id

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(
                url_for(
                    "users.profile",
                    id=usuario.id
                )
            )

        flash(
            "Correo o contraseña incorrectos.",
            "error"
        )

    return render_template(
        "login.html",
        form=form
    )


@users_bp.route("/logout")
def logout():

    session.pop(
        "user_id",
        None
    )

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("users.index")
    )


@users_bp.route(
    "/profile/<int:id>"
)
@login_required
def profile(id):

    usuario = User.query.get_or_404(id)

    return render_template(
        "profile.html",
        usuario=usuario
    )


@users_bp.route(
    "/profile/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_profile(id):

    usuario = User.query.get_or_404(id)

    form = EditUserForm(
        obj=usuario
    )

    if form.validate_on_submit():

        correo_existente = User.query.filter(
            User.email == form.email.data,
            User.id != usuario.id
        ).first()

        if correo_existente:

            flash(
                "Ese correo ya pertenece a otro usuario.",
                "error"
            )

            return render_template(
                "edit_profile.html",
                form=form,
                usuario=usuario
            )

        usuario.username = form.username.data
        usuario.email = form.email.data

        db.session.commit()

        flash(
            "Perfil actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "users.profile",
                id=usuario.id
            )
        )

    return render_template(
        "edit_profile.html",
        form=form,
        usuario=usuario
    )


@users_bp.route(
    "/profile/<int:id>/delete",
    methods=["POST"]
)
@login_required
def delete_profile(id):

    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    if session.get("user_id") == id:
        session.pop(
            "user_id",
            None
        )

    flash(
        "Usuario eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("users.index")
    )