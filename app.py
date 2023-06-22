import os

from flask import Flask, render_template, redirect, session, request

from flask_security import (
    Security,
    current_user,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
)
from database import db_session, init_db
from models.auth import User, Role

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

from Scripts.executeConsAgua import ResultadoDF

from pandas import DataFrame
from pandas import read_excel
path = os.getcwd()

# Create app
app = Flask(__name__)
app.config["DEBUG"] = True

app.config["UPLOAD_FOLDER"] = "uploads"

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


# Support for file upload
def get_upload_folder():
    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder


def save_file(file_form):
    folder = get_upload_folder()  # Create the upload folder if necessary
    filename = secure_filename(file_form.filename)
    if filename != "":
        file_path = os.path.join(folder, filename)
        file_form.save(file_path)
        return file_path
    return None


# Forms
class MyForm(FlaskForm):
    am_01_equi = FileField("am_01_equi")
    am_01_form = FileField("am_01_form")
    am_01_peukert = FileField("am_01_peukert")
    am_01_qdca_mainres = FileField("am_01_qdca_mainres")
    am_01_qdca = FileField("am_01_qdca")
    am_01_recarga_dhc = FileField("am_01_recarga_dhc")
    am_01_recarga_qdca = FileField("am_01_recarga_qdca")
    am_01_recarga_dch_prot = FileField("am_01_recarga_dch_prot")
    am_02_equi = FileField("am_02_equi")
    am_02_form = FileField("am_02_form")
    am_02_peukert = FileField("am_02_peukert")
    am_02_qdca_mainres = FileField("am_02_qdca_mainres")
    am_02_qdca = FileField("am_02_qdca")
    am_02_alta_dca = FileField("am_02_alta_dca")
    am_02_qdca = FileField("am_02_qdca")
    am_02_dch_prot = FileField("am_02_dch_prot")
    am_03_agua = FileField("am_03_agua")
    am_03_equi = FileField("am_03_equi")
    am_03_form = FileField("am_03_form")
    am_03_pol = FileField("am_03_pol")
    am_04_cons = FileField("am_04_cons")
    am_04_equi = FileField("am_04_equi")
    am_04_form = FileField("am_04_form")
    am_04_pol = FileField("am_04_pol")
    am_05_equi = FileField("am_05_equi")
    am_05_form = FileField("am_05_form")
    am_05_peukert = FileField("am_05_peukert")
    am_05_qdca_mainres = FileField("am_05_qdca_mainres")
    am_05_qdca = FileField("am_05_qdca")
    am_05_rec_alta_dch = FileField("am_05_rec_alta_dch")
    am_05_rec_qdca = FileField("am_05_rec_qdca")
    am_05_alta_dch = FileField("am_05_alta_dch")
    am_06_equi = FileField("am_06_equi")
    am_06_form = FileField("am_06_form")
    am_06_peukert = FileField("am_06_peukert")
    am_06_qdca_mainres = FileField("am_06_qdca_mainres")
    am_06_qdca = FileField("am_06_qdca")
    am_06_rec_alta_dch = FileField("am_06_rec_alta_dch")
    am_06_rec_qdca = FileField("am_06_rec_qdca")
    am_06_alta_dch = FileField("am_06_alta_dch")
    am_07_consu = FileField("am_07_consu")
    am_07_equi = FileField("am_07_equi")
    am_07_form = FileField("am_07_form")
    am_07_pola = FileField("am_07_pola")
    am_08_consu = FileField("am_08_consu")
    am_08_equi = FileField("am_08_equi")
    am_08_form = FileField("am_08_form")
    am_08_pola = FileField("am_08_pola")
    upload = SubmitField("upload")


# Views
@app.route("/dac")
@auth_required()
def dac():
    nome = "Neto"
    resultado = 10 + 10
    return render_template("dac.html", nome=nome, dado=resultado)


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
        valuesVector.append(float(value))

    dictKeys = []
    for key in form_data.keys():
        nome = key.replace("P_F","")
        nome = nome.replace("P_I","")
        if nome not in dictKeys:
            dictKeys.append(nome)
    
    index = 0
    nomeProt = []
    valuesProt = []

    for key in dictKeys:
        objConsAgua.addToDataFrame(protName=key, pesoInicial=valuesVector[index], peso=valuesVector[index + 1], cpValue=protValues[key])
        nomeProt.append(key)
        valuesProt.append(round(((valuesVector[index] - valuesVector[index + 1])/float(protValues[key]))*1000,3))
        index += 2

    from Scripts.generateGraph import generateComparationGraph
    generateComparationGraph(valuesProt, nomeProt)

    return redirect("/consumo/results/showresults")

@app.route("/consumo/results/showresults", methods=['GET'])
@auth_required()
def consumo_show():
    dataFramePandas = DataFrame(objConsAgua.getDataframeValue())
    dataFramePandas.to_excel(path + '/Results/Resultados_Cons_Água.xlsx', index=False)
    df = read_excel(path + '/Results/Resultados_Cons_Água.xlsx')
    html_table = df.to_html()

    cpValues = []
    protNames = []
    for key in protValues.keys():
        protNames.append(key)
        cpValues.append(protValues[key]) 

    return render_template('consumo_showresults.html', table=html_table, cpvalues=cpValues, protnames=protNames)


@app.route("/success")
@auth_required()
def success():
    check_file = os.path.exists(session["am_01_equi"])
    print(f"the file exists? {check_file}")
    return render_template("success.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/home")
@auth_required()
def home():
    form = MyForm()

    if form.validate_on_submit():
        file_list = [
            ("am_01_equi", form.am_01_equi.data),
            ("am_01_form", form.am_01_form.data),
            ("am_01_peukert", form.am_01_peukert.data),
            ("am_01_qdca_mainres", form.am_01_qdca_mainres.data),
            ("am_01_qdca", form.am_01_qdca.data),
            ("am_01_recarga_dhc", form.am_01_recarga_dhc.data),
            ("am_01_recarga_qdca", form.am_01_recarga_qdca.data),
            ("am_01_recarga_dch_prot", form.am_01_recarga_dch_prot.data),
            ("am_02_equi", form.am_02_equi.data),
            ("am_02_form", form.am_02_form.data),
            ("am_02_peukert", form.am_02_peukert.data),
            ("am_02_qdca_mainres", form.am_02_qdca_mainres.data),
            ("am_02_alta_dca", form.am_02_alta_dca.data),
            ("am_02_qdca", form.am_02_qdca.data),
            ("am_02_dch_prot", form.am_02_dch_prot.data),
            ("am_03_agua", form.am_03_agua.data),
            ("am_03_equi", form.am_03_equi.data),
            ("am_03_form", form.am_03_form.data),
            ("am_03_pol", form.am_03_pol.data),
            ("am_04_cons", form.am_04_cons.data),
            ("am_04_equi", form.am_04_equi.data),
            ("am_04_form", form.am_04_form.data),
            ("am_04_pol", form.am_04_pol.data),
            ("am_05_equi", form.am_05_equi.data),
            ("am_05_form", form.am_05_form.data),
            ("am_05_peukert", form.am_05_peukert.data),
            ("am_05_qdca_mainres", form.am_05_qdca_mainres.data),
            ("am_05_qdca", form.am_05_qdca.data),
            ("am_05_rec_alta_dch", form.am_05_rec_alta_dch.data),
            ("am_05_rec_qdca", form.am_05_rec_qdca.data),
            ("am_05_rec_alta_dch", form.am_05_rec_alta_dch.data),
            ("am_06_equi", form.am_06_equi.data),
            ("am_06_form", form.am_06_form.data),
            ("am_06_peukert", form.am_06_peukert.data),
            ("am_06_qdca_mainres", form.am_06_qdca_mainres.data),
            ("am_06_qdca", form.am_06_qdca.data),
            ("am_06_rec_alta_dch", form.am_06_rec_alta_dch.data),
            ("am_06_rec_qdca", form.am_06_rec_qdca.data),
            ("am_06_alta_dch", form.am_06_alta_dch.data),
            ("am_07_consu", form.am_07_consu.data),
            ("am_07_equi", form.am_07_equi.data),
            ("am_07_form", form.am_07_form.data),
            ("am_07_pola", form.am_07_pola.data),
            ("am_08_consu", form.am_08_consu.data),
            ("am_08_equi", form.am_08_equi.data),
            ("am_08_form", form.am_08_form.data),
            ("am_08_pola", form.am_08_pola.data),
        ]
        for file in file_list:
            path = save_file(file[1])
            session[file[0]] = path
        return redirect("/success")
    return render_template("index.html", form=form, name=current_user.email)


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
    app.run(port=5500)


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
