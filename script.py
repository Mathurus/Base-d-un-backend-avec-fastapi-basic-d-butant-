import json
import base64
from fastapi import FastAPI, HTTPException   #import des librairies
import uvicorn
from uvicorn.config import LOGGING_CONFIG
app = FastAPI()

@app.get("/configuration")   #toute le code qui suivrat sera éxécuter que si il y a une requete vers /configuration 
def root():
    with open("package.json", "rt") as f:   #ouvre le fichier package.json avec les droits de lecture 
        c = json.load(f)       #charge au format json les informations 
        return c    #retourne la variable c 

local_users = [
    {"name": "user1",
     "password": "quelquechose"}, #Dictionnaire des username et des password qui simule une base de donnée  
    {"name": "user2",
     "password": "autrechose"}
]

key = "dezdezzedzehdeoizdhzeoihzi"  #clé qui nous servirat pour un token plus tard 

def chiffre(name, key):
    return base64.b64encode(json.dumps({"name": name, "date_expiration": "2025"}).encode()) #génération du token 

def verifie_token(b64token, key):
    token = base64.b64decode(b64token).decode() #vérification du token 
    c = json.loads(token)
    return "name" in c


@app.get("/login")     #action pour le /login 
def login(name:str, password:str):
    print("name", name, password)  #affiche le user et son mot de passe 
    for user in local_users:
        if name == user['name']:    #vérifie si le user éxiste 
            print("Utilisateur trouvé") #si il éxiste il renvoie "Utilisateur trouvé "
            if password == user['password']:    #vérifie que le password correspond par rapport au user 
                return chiffre(name, "dezdezzedzehdeoizdhzeoihzi")  #si ça correspond il génère le token avec les informations correspondant  
            else:
                raise HTTPException(status_code=403, detail="Mot de passe erroné")  #sinon il renvoie une erreur 
    else:
        return 404, "Non trouvé"


def get_current_user():
    return "Mathurin"

@app.get("/users")  #action pour le /users
def users(token):
    # SQL-> BDD Utilisateurs
    #
    if verifie_token(token, key):   #si le user a un token valide ou spécifique (root) 
        return [{"name": "user1"}, {"name": "user2"}]   #il renvoie le nom des user 
    else:
        return "Accès interdit" #sinon il affiche accès interdit 


if __name__ == '__main__':
    import copy
    uvicorn.run(app)    #lancement de l'application     