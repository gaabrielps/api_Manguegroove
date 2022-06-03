#importe das bibliotecas e parametros da api
#response: retornos da nossa api #request: entrada de dados
from flask import Flask, Response, request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false #tratar com o banco de bados
import mysql.connector
import json


#iniciar api e configurações
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/deslizaHelp'

#criar a tabela de forma automatica
db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    cep = db.Column(db.String(50))
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    #traduzindo para json para rodar nossa api
    def toJsonUser(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "cep" : self.cep,
            "password" : self.password,
            "phone" : self.phone
        }

class Datas(db.Model):
    idEevent = db.Column(db.Integer, primary_key = True)
    mmInHours = db.Column(db.Integer)
    mmAccumulation = db.Column(db.Integer)
    nivelAlert = db.Column(db.Integer)

    def toJsonDatas(self):
        return {
        "idEevent": self.idEevent,
        "mmInHours" : self.mmInHours,
        "mmAccumulation" : self.mmAccumulation,
        "nivelAlert" : self.nivelAlert
        }


#criando rotas

#selecionar tudo
@app.route("/listUsers", methods=["GET"])
def allUsers():
    usersObj = Usuarios.query.all()
    #traduzindo para json
    usersJson = [user.toJsonUser() for user in usersObj] # para cada usuario(user) da lista de usuarios(usersObj), sera feito a função toJsonUser() 
    return geraResponse(200, 'Usuarios', usersJson, 'lista de usuarios atualizada')


@app.route("/listDatas", methods=["GET"])
def allDatas():    
    datasObj = Datas.query.all()
    datasJson = [data.toJsonDatas() for data in datasObj]
    
    return geraResponse(200, 'Dados', datasJson, 'lista de dados atualizados' )


#selecionar um
@app.route("/user/<id>", methods=["GET"])
def oneUser(id):
    userObj = Usuarios.query.filter_by(id=id).first()
    userJson = userObj.toJsonUser()

    return geraResponse(200, 'usuario', userJson)


@app.route("/data/<idEevent>",  methods=["GET"])
def onedata(idEevent):
    dataObj = Datas.query.filter_by(idEevent=idEevent).first()
    dataJson = dataObj.toJsonDatas()

    return geraResponse(200, 'dado',dataJson )


#cadastrar
@app.route("/signUser", methods=["POST"])
def signUser():
    body = request.get_json()
    #para gerar validação no cadastramento do usuário
    try:
        usuario = Usuarios(
            name=body["name"],
            email=body["email"], 
            cep=body["cep"], 
            password=body["password"],
            phone=body["phone"])
        db.session.add(usuario)
        db.session.commit()
        return geraResponse(200, 'usuario', usuario.toJsonUser(), 'cadastrado com sucesso!')

    except Exception as e:
        print(e)
        return geraResponse(400, 'usuario', {}, 'Erro ao cadastrar')



@app.route("/inputDatas", methods=["POST"])
def inputDatas():
    body = request.get_json()
    #para gerar validação no cadastramento do usuário

    try:
        data = Datas(
            mmInHours=body["mmInHours"],
            mmAccumulation=body["mmAccumulation"],
            nivelAlert=body["nivelAlert"])
        db.session.add(data)
        db.session.commit()
        return geraResponse(200, 'data', data.toJsonDatas(), 'sucesso na entrada de dados de risco!')
    except Exception as e:
        print('Erro', e)
        return geraResponse(400, 'data', {}, 'Erro ao cadastrar um novo dado de risco')



#Atualizar usuário
@app.route("/user/<id>", methods=["PUT"])
def updateUser(id):
    userObj = Usuarios.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('name' in body):
            userObj.name = body["name"]

        if('email' in body):
            userObj.email = body["email"]

        if('cep' in body):
            userObj.cep = body["cep"]

        if('password' in body):
            userObj.password = body["password"]

        if('phone' in body):
            userObj.phone = body["phone"]
        
        db.session.add(userObj)
        db.session.commit()
        return geraResponse(200, 'usuario', userObj.toJsonUser(), 'Atualizado com sucesso!')
        
    except Exception as e:
        print('Erro', e)
        return geraResponse(400, 'usuario', {}, 'Erro ao atualizar')


#Atualizar dados 
@app.route("/data/<idEevent>",  methods=["PUT"])
def updateDatas(idEevent):

    dataObj = Datas.query.filter_by(idEevent=idEevent).first()
    body = request.get_json()

    try:

        if('mmInHours' in body):
            dataObj.mmInHours = body["mmInHours"]

        if('mmAccumulation' in body):
            dataObj.mmAccumulation = body["mmAccumulation"]

        if('nivelAlert' in body):
            dataObj.nivelAlert = body["nivelAlert"]

        db.session.add(dataObj)
        db.session.commit()
        return geraResponse(200, 'dados', dataObj.toJsonDatas(), 'Atualizar dados de risco!')
        
    except Exception as e:
        print('Erro', e)
        return geraResponse(400, 'dados', {}, 'Erro ao atualizar dados de risco!')


#Deletar
@app.route("/user/<id>", methods=["DELETE"])
def deleteUser(id):
    userObj = Usuarios.query.filter_by(id=id).first()

    try:
        db.session.delete(userObj)
        db.session.commit()
        return geraResponse(200, 'usuario', userObj.toJsonUser(), 'Deletado com sucesso!')
        
    except Exception as e:
        print('Erro', e)
        return geraResponse(400, 'usuario', {}, 'Erro ao deletado')


@app.route("/data/<idEevent>", methods=["DELETE"])
def deleteData(idEevent):
    dataObj = Datas.query.filter_by(idEevent=idEevent).first()

    try:
        db.session.delete(dataObj)
        db.session.commit()
        return geraResponse(200, 'dado', dataObj.toJsonDatas(), 'Deletado com sucesso!')
        
    except Exception as e:
        print('Erro', e)
        return geraResponse(400, 'dado', {}, 'Erro ao deletado')


#função para retornar mensagens de erro ou nao e traduzir todas as rotas para JSON 
def geraResponse(status, nameContent, content, message= False):
    body = {}
    body[nameContent] = content

    if (message):
        body["mensagem"] = message

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()