import os
import base64
import pickle
from flask import abort

base_dir ='data/'

#configura a área do usuário
def configure_workspace(idUsuario):
    workspace = base_dir+idUsuario
    images = workspace + '/images/'
    image_base = images + '/base/'
    image_auth = images + '/auth/'
    matrix = workspace + '/matrix/'
    
    if not os.path.exists(os.path.dirname(workspace)):
        try:
            os.makedirs(os.path.dirname(workspace))
            os.makedirs(os.path.dirname(images))
            os.makedirs(os.path.dirname(image_base))
            os.makedirs(os.path.dirname(image_auth))
            os.makedirs(os.path.dirname(matrix))
        except OSError as ex:
            abort(400)

#salva as imagens
def save_images(fullPath, image):    
    try:
        with open(fullPath, "wb") as fh:
            fh.write(base64.standard_b64decode(image))
    except IOError as io:
        abort(400)
    finally:
        fh.close()

#salva a matriz gerada
def save_matrix(fullPath, data):
    try:    
        with open(fullPath, "wb") as fh:
            fh.write(pickle.dumps(data))
    except IOError as io:
        abort(400)
    finally:
        fh.close()

#metodo verify para verificar se o diretorio e o arquivo solicitados existem no caminho

