class Config:
    SECRET_KEY = "clave-secreta-proyecto"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:Chino1015.@localhost:3306/usuarios_flask"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False