from pymongo import MongoClient

def connect(collection):
    try:
        client = MongoClient('mongodb://10.222.18.110:27017')
        db = client['reconhecimento-facial']
        collection =  db[collection]
        
        return collection
    except:
        abort(400)

def insereDB(obj, collection):
    conn = connect(collection)    
    conn.insert_one(obj)

def get_users(collection):
    conn = connect(collection)
    return conn.find() 
    
def get_user(idUsuario, collection):
    conn = connect(collection)
    return conn.find_one({'idUsuario': idUsuario})
