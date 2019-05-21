from flask import jsonify
import providers.provider as provide
from bson.json_util import dumps
import utils.util as util
from datetime import datetime
from ai.ai import generate_matrix, facial_auth

collection_users = 'tabUsers'
collection_auth = 'tabAuth'

#retorna a lista de usuários cadastrados na base
def get_users():
    users = provide.get_users(collection_users)
    if(users.count() >0):
        return dumps(provide.get_users(collection_users)),200
    else:
        return jsonify({"mensagem":"Nenhum usuário encontrado"}),404

#retorna um usuário na base ou nulo se não existe
def get_user(idUsuario):
    user = provide.get_user(str(idUsuario), collection_users)
    if(user is not None):
        return dumps(user),200
    else:
        return jsonify({"menssagem":"Usuário não encontrado"}),404

#adiciona o usuário na base e grava a foto do usuário no HDFS
def add_user(idUsuario, usuario):
    #trata os parâmetros de entrada
    idUsuario = str(idUsuario)
    coop = str(usuario["cooperativa"])
    conta = str(usuario["conta"])    
    nome = usuario["nome"]
    imagem = usuario["imagem"]
    base = imagem.split(",")[1]

    #define a workspace do usuário
    user_path = util.base_dir+idUsuario+"/"
    user_images = user_path+"images/base/"
    nome_imagem = "base_image_"+str(datetime.now()).replace(" ","_")+".jpeg"
    fullpath = user_images+nome_imagem
    
    #cria o objeto para inserir no banco 
    obj = {}
    obj['idUsuario'] = idUsuario
    obj['cooperativa'] = coop
    obj['conta'] = conta
    obj['nome'] = nome
    obj['imagem_base'] = fullpath

    user = provide.get_user(str(idUsuario), collection_users)
    if(user is None):
        #salva a imagem base de autenticação na workspace do usuário
        util.configure_workspace(idUsuario)        
        util.save_images(fullpath, base)
        obj['matrix_base'] = generate_matrix(obj)
        provide.insereDB(obj, collection_users)
        return jsonify({"messagem":"Usuario criado"}),201
    else:
        return jsonify({"mensagem":"Usuário com esse ID já existe"}),409

def user_auth(idUsuario, usuario):
    #trata os parâmetros de entrada
    idUsuario = str(idUsuario)
    coop = str(usuario["cooperativa"])
    conta = str(usuario["conta"])    
    nome = usuario["nome"]
    imagem = usuario["imagem"]
    base = imagem.split(",")[1]

    user_path = util.base_dir+idUsuario
    user_images = user_path+"/images/auth/"
    nome_imagem = "auth_image_"+str(datetime.now()).replace(" ","_")+".jpeg"
    fullpath = user_images+nome_imagem

    user = provide.get_user(str(idUsuario), collection_users)
    if(user is not None):
        util.save_images(fullpath, base)
        user = provide.get_user(idUsuario, collection_users)
        match = facial_auth(fullpath, user['matrix_base'])
        
        obj = {}
        obj['idUsuario'] = idUsuario
        obj['nome'] = nome
        obj['dth_auth'] = str(datetime.now()).replace(" ","_")
        obj['imagem'] = fullpath
        obj['match'] = str(match[0])

        if(match):
            provide.insereDB(obj, collection_auth)
            return jsonify({"messagem":"Usuário reconhecido"}),200
        else:
            provide.insereDB(obj, collection_auth)
            return jsonify({"messagem":"Usuário não reconhecido"}),403  
    else:
        return jsonify({"messagem":"Nenhum usuário encontrado com esse ID"}),404