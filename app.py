import os

from flask import Flask, render_template
from flask_security import (
    Security,
    current_user,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
)
from database import db_session, init_db
from models.auth import User, Role

from Scripts.executeConsAgua import getDataframeValue
data_Cons_Agua = getDataframeValue()

# Create app
app = Flask(__name__)
app.config["DEBUG"] = True

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


# Views
@app.route("/dac")
@auth_required()
def dac():
    return render_template("dac.html")


@app.route("/polarizacao")
@auth_required()
def polarizacao():
    return render_template("polarizacao.html")


@app.route("/pekeurt")
@auth_required()
def pekeurt():
    return render_template("pekeurt.html")

@app.route("/consumo")
@auth_required()
def consumo():
    data = data_Cons_Agua
    keys = []
    for key in data.keys():
        keys.append(key)

    return render_template("consumo.html", coluna1=data[keys[0]][0], coluna2=data[keys[0]][1], coluna3=data[keys[0]][2], coluna4=data[keys[0]][3],
                           l11=data[keys[1]][0], l12=data[keys[1]][1], l13=data[keys[1]][2], l14=data[keys[1]][3],
                           l21=data[keys[2]][0], l22=data[keys[2]][1], l23=data[keys[2]][2], l24=data[keys[2]][3],
                           l31=data[keys[3]][0], l32=data[keys[3]][1], l33=data[keys[3]][2], l34=data[keys[3]][3],
                           l41=data[keys[4]][0], l42=data[keys[4]][1], l43=data[keys[4]][2], l44=data[keys[4]][3])


@app.route("/")
@app.route("/home")
@auth_required()
def home():
    return render_template("index.html", name=current_user.email)
    # return render_template_string("Hello {{email}} !", email=current_user.email)


# one time setup
with app.app_context():
    # Create a user to test with
    init_db()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(
            email="test@me.com", password=hash_password("password")
        )
    db_session.commit()
    db_session.close()

if __name__ == "__main__":
    # run application (can also use flask run)
    app.run()


@app.cli.command("create-user")
def create_user():
    """Criar um usuario."""
    email = input("Coloque o seu email: ")
    password = hash_password(input("Coloque o password: "))
    confirm_password = hash_password(input("Coloque o password novamente: "))
    if password != confirm_password:
        print("Passwords diferentes")
        return 1
    try:
        app.security.datastore.create_user(email=email, password=password)
        db_session.commit()
        print(f"Usuario com email {email} criado com sucesso!")
    except Exception as e:
        print("Nao foi possivel criar o usuario.")
        print(e)
