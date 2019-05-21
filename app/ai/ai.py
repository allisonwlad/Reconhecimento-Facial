import utils.util as util
import cv2
import face_recognition 
from datetime import datetime
import pickle

def generate_matrix(obj):
    #inicia as variáveis de apoio
    knownEncodings = []
    knownNames = []
    
    #inicia a workspace do usuário e carrega a imagem base para gerar a matriz
    matrix_dir = util.base_dir+obj['idUsuario']+"/matrix/"
    matrix_file = matrix_dir+str(obj['idUsuario'])+"_"+str(datetime.now()).replace(" ","_")+".pickle"
    image_in = cv2.imread(obj['imagem_base'])
    #converte a imagem para RGB
    rgb = cv2.cvtColor(image_in, cv2.COLOR_BGR2RGB)
    #Chama o modelo para reconecimento de rostos nas imagens
    boxes = face_recognition.face_locations(rgb, model="cnn")
    #cria o encoding da face
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(obj['idUsuario'])

    data = {"encodings":knownEncodings, "name":knownNames}
    util.save_matrix(matrix_file, data)
    
    return matrix_file

def facial_auth(img_auth, base_matrix):
        
    # carrega base de conhecimento
    data = pickle.loads(open(base_matrix, "rb").read())

    # carrega imagem e transforma para RGB para o dlib()
    image_in = cv2.imread(img_auth)
    rgb = cv2.cvtColor(image_in, cv2.COLOR_BGR2RGB)
        
    # detecta o rosto na imagem
    boxes = face_recognition.face_locations(rgb, model="cnn") 
    
    # retorna as coordenadas da face na imagem e codifica para comparação
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        # compara as faces
        matches = face_recognition.compare_faces(data["encodings"], encoding)

    return matches
     