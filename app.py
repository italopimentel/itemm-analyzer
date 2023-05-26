import os

from flask import Flask, render_template, redirect
from flask import request
from flask_security import (
    Security,
    current_user,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
)
from database import db_session, init_db
from models.auth import User, Role

from Scripts.executeConsAgua import ResultadoDF

from pandas import DataFrame
from pandas import read_excel
path = os.getcwd()

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

@app.route("/consumo", methods=['GET'])
@auth_required()
def consumo():
    return render_template("consumo.html")

objConsAgua = ResultadoDF()
protValues = {}

#metódo responsável por receber os envios de arquivo
@app.route("/consumo", methods=['POST'])
@auth_required()
def consumo_post():
    for planilha in os.listdir(path + "/Sheets/"):
        os.remove(path + "/Sheets/" + planilha)

    arquivos = request.files.getlist('arquivos')
    for arquivo in arquivos:
        arquivo.save(path + "/Sheets/" + arquivo.filename)
    
    protValues.clear()
    return redirect("/consumo/results")

@app.route("/consumo/results", methods=['GET'])
@auth_required()
def consumo_results_get():
    global protValues
    for plan_csv in os.listdir(path + '/Sheets/'):
        if plan_csv.endswith('.csv') == True:
            valuesExtracted = objConsAgua.calculateCP(plan_csv)
            protValues[valuesExtracted[0]] = valuesExtracted[1]

    protNames = protValues.keys()
    return render_template("consumo_results.html", protNames=protNames)


#recebe os dados enviados do formulário de sub listas
@app.route("/consumo/results", methods=['POST'])
@auth_required()
def consumo_results_post():
    form_data = request.form
    valuesVector = []
    for nome, value in form_data.items():
        print(value)
        valuesVector.append(float(value))

    dictKeys = []
    for key in form_data.keys():
        nome = key.replace("P_F","")
        nome = nome.replace("P_I","")
        print(nome)
        if nome not in dictKeys:
            dictKeys.append(nome)
    
    print(dictKeys)
    index = 0
    for key in dictKeys:
        objConsAgua.addToDataFrame(protName=key, pesoInicial=valuesVector[index], peso=valuesVector[index + 1], cpValue=protValues[key])
        index += 2
    
    print (objConsAgua.getDataframeValue())
    return redirect("/consumo/results/showresults")

@app.route("/consumo/results/showresults", methods=['GET'])
@auth_required()
def consumo_show():
    dataFramePandas = DataFrame(objConsAgua.getDataframeValue())
    dataFramePandas.to_excel(path + '/Results/Resultados_Cons_Água.xlsx', index=False)
    df = read_excel(path + '/Results/Resultados_Cons_Água.xlsx')
    html_table = df.to_html()
    return render_template('consumo_showresults.html', table=html_table)

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
